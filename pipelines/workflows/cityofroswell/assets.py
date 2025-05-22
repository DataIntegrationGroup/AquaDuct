import dagster as dg
from dagster_gcp.gcs import GCSResource

# ------------------------------------------------------------------------------
# Asset: get_csv_from_gcs
# ------------------------------------------------------------------------------
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
