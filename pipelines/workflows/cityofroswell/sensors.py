import dagster as dg
from google.cloud import storage
from pipelines.utils.secrets import GCP_PROJECT_NUM
from .partitions import file_partitions

@dg.sensor(
        job_name="__ASSET_JOB",
        minimum_interval_seconds=300,
        default_status=dg.DefaultSensorStatus.RUNNING
        )
def cityofroswell_sensor(context):
    """
    Sensor to monitor the GCS bucket for new files and trigger the asset if a new file is found.
    """
    client = storage.Client(project=str(GCP_PROJECT_NUM))
    bucket = client.bucket("roswellbubbler_dev")
    context.log.info(f"Monitoring bucket: {bucket.name}")
    
    known_files = set(context.instance.get_dynamic_partitions(file_partitions.name))

    for blob in bucket.list_blobs(prefix="observations_"):
        if blob.name not in known_files:
            context.log.info(f"New file detected: {blob.name}")
            # Trigger the asset by adding a new partition
            context.instance.add_dynamic_partitions(
                file_partitions.name,
               [blob.name],
            )
            yield dg.RunRequest(partition_key=blob.name)
        else:
            context.log.info(f"File already processed: {blob.name}")
       
    