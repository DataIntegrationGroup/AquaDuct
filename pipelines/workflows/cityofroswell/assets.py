import dagster as dg
import frost_sta_client as fsc


FROST_URL = "http://localhost:8080/FROST-Server/v1.1" #TODO: move to a sensor things util.

# Get csv file from GCS bucket
@dg.asset(
    required_resource_keys={"gcs_roswell"},
)
def get_csv_from_gcs(context):
    # Get the GCS bucket and prefix from the context
    gcs = context.resources.gcs_roswell
    client = gcs.get_client()

    # Get the bucket and prefix from the GCS resource
    bucket = client.bucket(gcs.gcs_bucket)
    prefix = gcs.gcs_prefix
    context.log.info(f"Fetching CSV files from bucket {bucket} with prefix {prefix}")

    blobs = bucket.list_blobs(prefix=gcs.gcs_prefix)
    context.log.info(f"Found {len(list(blobs))} blobs in bucket {gcs.gcs_bucket}")
    
    all_data = []
    for blob in blobs:
        context.log.info(f"Processing blob: {blob.name}")
        content = blob.download_as_text()
        all_data.append({
            "name": blob.name,
            "content": content,
            "updated": blob.updated
        })

    return all_data
