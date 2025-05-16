import dagster as dg
import requests
from pipelines.utils.auth import OAuth2
import json
# import frost_sta_client as fsc

location_partitions = dg.DynamicPartitionsDefinition(name="hydrovu_locations")

@dg.asset()
def hydrovu_locations(context):
  url = "https://www.hydrovu.com/public-api/v1/locations/list"
  auth = OAuth2(token_url='https://hydrovu.com/public-api/oauth/token', secret_name='hydrovu_pvacd')

  # st_url = "localhost:8080/FROST-Server/v1.1"
  # frost_service = fsc.SensorThingsService(st_url)

  headers={}
  next_page = True
  #TODO: abstract the fetching logic. On each request, check if we need to re-auth with Oauth2.
  while next_page:
    res = requests.get(url, auth=auth, headers=headers)
    for location in res.json():
      #TODO: this only adds partitions... need to recreate the whole set (in case some are deleted). are there downsides to this?
      context.instance.add_dynamic_partitions(location_partitions.name, [str(location['id'])])
      # context.instance.delete_dynamic_partitions(...)
    ##WRITE LOCATIONS TO sensorthings
    # st_loc = fsc.Location()

    next_page = res.headers.get('X-ISI-Next-Page')
    headers['X-ISI-Start-Page'] = next_page

@dg.asset(
    deps=[ hydrovu_locations ],
    partitions_def=location_partitions
)
def hydrovu_measurements_fetch(context):
  url = f"https://www.hydrovu.com/public-api/v1/locations/{context.partition_key}/data"
  auth = OAuth2(token_url='https://hydrovu.com/public-api/oauth/token', secret_name='hydrovu_pvacd')
  headers={}
  next_page = True
  #TODO: abstract fetching logic (same as in hydrovu_locations)
  while next_page:
    res = requests.get(url, auth=auth, headers=headers)
    next_page = res.headers.get('X-ISI-Next-Page')
    headers['X-ISI-Start-Page'] = next_page
  
@dg.asset(
    deps=[ hydrovu_measurements_fetch ],
)
def hydrovu_measurements_transform_load(context):
  pass