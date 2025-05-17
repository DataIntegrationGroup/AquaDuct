from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import pipelines.utils.secrets as secrets

class OAuth2():
  def __init__(self, token_url, secret_name):
    self.token_url = token_url
    self.secret = secrets.get(secret_name)
    self.client = BackendApplicationClient(client_id=self.secret['id'])
    self.oauth = OAuth2Session(client=self.client)
    self.token = self.fetch_new_token()

  def __call__(self, request):
    request.headers['Authorization'] = f'Bearer {self.token['access_token']}'
    return request

  def fetch_new_token(self):
    return self.oauth.fetch_token(token_url=self.token_url, client_id=self.secret['id'],
            client_secret=self.secret['secret'])


def is_token_expired(response):
  if response.status_code == 401:
    try:
      error_data = response.json()
      if error_data.get("error") == "invalid_token":
        return True
    except ValueError:
        pass  # Response is not JSON or does not contain expected fields
  return False