from dagster import Definitions, load_assets_from_modules
from pipelines.workflows.cityofroswell import assets
from pipelines.utils.secrets import GCP_PROJECT_NUM
from dagster_gcp.gcs import GCSResource
from . import assets, sensors

gcs_roswell = GCSResource(
    project=str(GCP_PROJECT_NUM),
    gcs_bucket="roswellbubbler_dev",  # TODO: move to env var or config
    gcs_prefix="observations",  # TODO: move to env var or config
)

defs = Definitions(
    assets=load_assets_from_modules([assets]),
    sensors=[sensors.cityofroswell_sensor],
    resources={
        # key **must** match the param name in the asset signature
        "gcs_roswell": gcs_roswell,
    },
)