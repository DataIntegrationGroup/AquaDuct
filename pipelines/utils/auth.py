from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import pipelines.utils.secrets as secrets

class AuthStrategy():
  def __init__(self):
    pass
  def apply(self, request):
    pass

class OAuth2(AuthStrategy):
  def __init__(self, token_url, secret_name):
    self.token_url = token_url
    secret = secrets.get(secret_name)
    self.secret = secret

  def __call__(self, request):
    client = BackendApplicationClient(client_id=self.secret['id'])
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=self.token_url, client_id=self.secret['id'],
            client_secret=self.secret['secret'])

    request.headers['Authorization'] = f'Bearer {token['access_token']}'
    return request