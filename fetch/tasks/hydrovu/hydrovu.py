from fetch.tasks.fetcher_task import FetcherTask
from fetch.auth import OAuth2

#if cron is used, fetch interval should default to since_last (if no last, backfill entire history?). i don't like this interval, since they are essentially the same field. just use cron?
# does this need to generate filenames? i've seen that in the past. e.g. given a start/end range of fetching, i need to generate specific filenames with dates in that range.
#if backfilling, use start/end interval
def hydrovu_fetch():
  pass

#TODO: generalize the auth part so it can fetch bernco and pvacd (they use separate ids/tokens)

base_url = "https://www.hydrovu.com/public-api/v1/locations/list"

class HydrovuTask(FetcherTask):
  def __init__(self, name):
    super.__init__(
      self,
      name = name,
      url = base_url,
      schedule = "5 0 * * *",  #etc... have a default of daily at 12:05
      auth = OAuth2(token_url='https://hydrovu.com/public-api/oauth/token'),
      # fetch = hydrovu_fetch
      # fetch_interval = "since_last" #either fetch from the previous fetch, or fetch a specific interval, like 1 day of data
    )


hydrovu_bernco = HydrovuTask(
  source_name = 'hydrovu_bernco',
  dataset = 'locations',
  url = f"{base_url}/locations/list",
)

hydrovu_bernco = HydrovuTask(
  source_name = 'hydrovu_bernco',
  dataset = 'locations',
  url = f"{base_url}/locations"
)

hydrovu_pvacd = HydrovuTask(
  name = 'hydrovu_pvacd'
)
