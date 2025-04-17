import utils.secrets as secrets
import requests
import fetch.auth

tasks = []

class DataQuantity():
  #the fetched quantity, abstract base class
  #use this to define things like 1 day, 5 pages, 100mb, "full_history" etc.
  # what about ranges, especially datetime?
  pass

class Days(DataQuantity):
  def __init__(self, num):
    pass

class DateRange(DataQuantity):
  def __init__(self, start, end):
    pass

class FetcherTask():
  def __init__(self, name, url, schedule, auth, fetch=None, amount=Days(1)):
    self.name = name
    self.url = url
    self.schedule = schedule
    self.rate_limit_rps = 0.5 #requests per second
    self.limit = amount
    self.auth = auth
    self.auth.task_name = name #TODO: find a cleaner way
    self.fetch = fetch if fetch else self._fetch
    self.amount_done = DataQuantity()
    tasks.append(self)

  def run(self):
    import pdb; pdb.set_trace()
    self.fetch()
    # for data in self.fetch():
      # gcs.write(data)

  def _fetch(self):
    #TODO: figure out the interface for pagination... should be easy to customize, and versatile. not sure what the base model should be...
    # maybe just allow user to override _fetch method. don't try to be too clever.
    # is it problematic to need to parse certain parts of a fetch to decide whether to fetch more? kind of breaks my model of loading later... oh well. keep it simple.
    import pdb; pdb.set_trace()
    # while self.amount < self.amount_done:
    #while p := _next_page():
    import pdb; pdb.set_trace()
    r = requests.get(self.url, auth=self.auth)
    # yield r
    import pdb; pdb.set_trace()
