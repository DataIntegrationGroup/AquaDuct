from google.cloud import secretmanager
import json
import utils.env as env

DEFAULT_PROJECT_NUM = env.get("GCP_PROJECT_NUM")

def get(secret_id, project_id=DEFAULT_PROJECT_NUM):
  client = secretmanager.SecretManagerServiceClient()
  name = f'projects/{project_id}/secrets/{secret_id}/versions/latest'
  response = client.access_secret_version(request={"name": name})
  return json.loads(response.payload.data)