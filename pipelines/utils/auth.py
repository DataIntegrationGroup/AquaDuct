from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import pipelines.utils.secrets as secrets

##TODO: instead make auth a decorator for requests?
class AuthStrategy():
  def __init__(self):
    pass
  def apply(self, request):
    pass

class OAuth2(AuthStrategy):
  def __init__(self, token_url):
    self.token_url = token_url

  def __call__(self, request):
    secret = secrets.get(self.task_name)
    client_id, client_secret = secret['id'], secret['secret']

    client = BackendApplicationClient(client_id=secret['id'])
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=self.token_url, client_id=client_id,
            client_secret=client_secret)

    request.headers['Authorization'] = f'Bearer {token['access_token']}'
    return request