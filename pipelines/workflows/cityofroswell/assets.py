import dagster as dg
from dagster_gcp.gcs import GCSResource

# ------------------------------------------------------------------------------
# Asset: get_csv_from_gcs
# ------------------------------------------------------------------------------

# TODO: 5/23/2025 - Add parition file to create partitions after csv load
# TODO: 5/23/2025 - Setup a shared reources file for GCS assets (or single asset?)
# TODO: 5/23/2025 - Implement FROST API to load parition into SensorThings
# TODO: 5/23/2025 - Implement dagster sensor to watch for new files
# TODO: 5/23/2025 - Update definitions at the workflow level to include all resouces and sensors
# TODO: 5/23/2025 - Move any reusable code to utils

@dg.asset
def get_csv_from_gcs(
    context: dg.AssetExecutionContext,
    gcs: GCSResource):
    client = gcs.get_client()

    bucket = client.bucket("roswellbubbler_dev") 
    prefix = "observations"

    blobs = list(bucket.list_blobs(prefix=prefix))
    context.log.info("Found %d blobs in gs://%s/%s", len(blobs), bucket.name, prefix)

    return [
        {
            "name": blob.name,
            "content": blob.download_as_text(), 
            "updated": blob.updated,
        }
        for blob in blobs
    ]
