import dagster as dg
from dagster_gcp.gcs import GCSResource
from pipelines.utils.resources import SensorThingsResource
from .partitions import file_partitions

# ------------------------------------------------------------------------------
# Asset: get_csv_from_gcs
# ------------------------------------------------------------------------------

# TODO: 5/23/2025 - Implement FROST API to load parition into SensorThings
# TODO: 5/23/2025 - Implement dagster sensor to watch for new files
# TODO: 5/23/2025 - Update definitions at the workflow level to include all resouces and sensors
# TODO: 5/23/2025 - Move any reusable code to utils

@dg.asset(partitions_def=file_partitions)
def get_csv_from_gcs(
    context,
    gcs_roswell: GCSResource
    ):
    
    client = gcs_roswell.get_client()

    bucket = client.bucket("roswellbubbler_dev") 

    blob = bucket.blob(context.partition_key)

    context.log.info("Fetching blobs from gs://%s/", bucket.name)
    context.log.info("Found blob: %s", blob.name)

    content = blob.download_as_text()
    context.add_output_metadata({"gcs_generation": blob.generation})

    return content

# ------------------------------------------------------------------------------

@dg.asset(partitions_def=file_partitions, deps=[get_csv_from_gcs])
def load_csv_to_sensorthings(
    context,
    get_csv_from_gcs,
    frost: SensorThingsResource
):
    st_client = frost.get_client()
    context.log.info("Loading CSV content to SensorThings")

