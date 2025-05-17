import dagster as dg
import requests
import json
import frost_sta_client as fsc
from pipelines.utils.auth import OAuth2, is_token_expired

HYDROVU_PVACD_URL = "https://www.hydrovu.com/public-api/v1/locations/"
HYDROVU_OAUTH_URL = 'https://hydrovu.com/public-api/oauth/token'
FROST_URL = "http://localhost:8080/FROST-Server/v1.1"

location_partitions = dg.DynamicPartitionsDefinition(name="hydrovu_locations")

def fetch_paginated(url, handle_page=None):
  auth = OAuth2(token_url=HYDROVU_OAUTH_URL, secret_name='hydrovu_pvacd')
  headers={}
  next_page = 'first page'
  responses = []
  while next_page:
    response = requests.get(url, auth=auth, headers=headers)
    responses.append(response)
    if handle_page:
      handle_page(response)

    if is_token_expired(response):
      auth.fetch_new_token()
    next_page = response.headers.get('X-ISI-Next-Page')
    headers['X-ISI-Start-Page'] = next_page
  return responses

def convert_location_hydrovu_to_sensorthings(loc):
  return fsc.Location(
    name=loc['name'],
    description="Location of well where measurements are made",
    properties={
      'agency': 'PVACD'
    },
    location={
      'type': 'Point',
      'coordinates': [loc['gps']['latitude'],
                      loc['gps']['longitude']]
    },
    encoding_type="application/geo+json")


@dg.asset()
def hydrovu_locations(context):
  url = HYDROVU_PVACD_URL + "list"
  frost_url = FROST_URL
  frost_service = fsc.SensorThingsService(frost_url)

  for response in fetch_paginated(url):
    partitions = []
    for loc in response.json():
      context.log.info(f"Writing location to FROST: { loc }")
      # TODO: how to upsert? this creates duplicates when re-run.
      frost_service.create(convert_location_hydrovu_to_sensorthings(loc))
      partitions.append(str(loc['id']))
    # TODO: delete old ones?
    context.log.info("Creating new partitions.")
    context.instance.add_dynamic_partitions(location_partitions.name, partitions)
    # context.instance.delete_dynamic_partitions(...)

@dg.asset(
    deps=[ hydrovu_locations ],
    partitions_def=location_partitions
)
def hydrovu_measurements_fetch(context):
  url = HYDROVU_PVACD_URL + f"{context.partition_key}/data"
  def process(response):
    context.pdb.set_trace()
  fetch_paginated(url, process)
  # for i, response in enumerate(fetch_paginated(url)):
  #   context.log.info(f"Fetching hydrovu measurements page {i} for location {context.partition_key}")
  #   context.pdb.set_trace()
  

@dg.asset(
    deps=[ hydrovu_measurements_fetch ],
)
def hydrovu_measurements_transform_load(context):
  pass