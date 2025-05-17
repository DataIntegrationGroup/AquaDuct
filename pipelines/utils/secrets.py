from google.cloud import secretmanager
import json
import pipelines.utils.env as env
import requests

def get_project_id():
  try:
    response = requests.get(
      'http://metadata.google.internal/computeMetadata/v1/project/project-id',
      headers={'Metadata-Flavor': 'Google'},
      timeout=3  # Add timeout to avoid hanging
    )
    response.raise_for_status()  # Raise exception for HTTP errors
    return response.text
  except (requests.RequestException, ConnectionError):
    # Fall back to environment variable if metadata server request fails
    import os
    project_id = env.get("GCP_PROJECT_NUM")
    if project_id:
        return project_id
    else:
      raise RuntimeError("Could not determine GCP project ID from metadata server or environment variables")

GCP_PROJECT_NUM = get_project_id()

def get(secret_id, project_id=GCP_PROJECT_NUM):
  client = secretmanager.SecretManagerServiceClient()
  name = f'projects/{project_id}/secrets/{secret_id}/versions/latest'
  response = client.access_secret_version(request={"name": name})
  return json.loads(response.payload.data)