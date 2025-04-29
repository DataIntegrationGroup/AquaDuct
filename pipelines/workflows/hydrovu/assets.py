import dagster as dg
import requests
from pipelines.utils.auth import OAuth2

# location_partitions = dg.DynamicPartitionsDefinition(name="locations")

@dg.asset
def hydrovu_tester():
    return 5

# @dg.asset
# def hydrovu_locations():
#     ### Can this generate the location partitions? (maybe unnecessary)

#     url = "https://www.hydrovu.com/public-api/v1/locations/list"
#     auth = OAuth2(token_url='https://hydrovu.com/public-api/oauth/token'),
#     response = requests.get(url, auth=auth)
#     pass

# @dg.asset(
#     deps=hydrovu_locations,
# )
# def hydrovu_measurements():
#     pass