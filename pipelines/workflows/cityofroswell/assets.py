import dagster as dg
from dagster_gcp.gcs import GCSPickleIOManager, GCSResource

import frost_sta_client as fsc
from pipelines.utils.secrets import GCP_PROJECT_NUM

FROST_URL = "http://localhost:8080/FROST-Server/v1.1" #TODO: move to a sensor things util.


# get data from GCS bucket for city of roswell
# gcs_pickle_io_manager = GCSPickleIOManager(
#   gcs=GCSResource(project=str(GCP_PROJECT_NUM)),
#   gcs_bucket="roswellbubbler_dev", #TODO: move to env var or config
#   gcs_prefix="observations"
# )

gcs = GCSResource(
    project=str(GCP_PROJECT_NUM),
    gcs_bucket="roswellbubbler_dev",  # TODO: move to env var or config
    gcs_prefix="observations"
)

@dg.asset(
    required_resource_keys={"gcs"},
    io_manager_key="in_memory",
    config_schema={
        "bucket": str,
        "prefix": str
    },
)
def get_csv_from_gcs(context):
    # Get csv file from GCS bucket
    bucket =  context.op_config["bucket"]
    prefix = context.op_config["prefix"]
    gcs_client = context.resources.gcs

    blobs = gcs_client.list_blobs(bucket, prefix=prefix)
    context.log.info(f"Found {len(blobs)} blobs in bucket {bucket} with prefix {prefix}")
    for blob in blobs:
        context.log.info(f"Found blob: {blob.name}")
    
    all_data = []
    for blob in blobs:
        content = blob.download_as_text()
        all_data.append({
            "name": blob.name,
            "content": content,
            "updated": blob.updated
        })

    return all_data
