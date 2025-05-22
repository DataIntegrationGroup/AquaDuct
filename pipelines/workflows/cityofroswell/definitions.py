from dagster import Definitions, load_assets_from_modules
from pipelines.workflows.cityofroswell import assets
from pipelines.utils.secrets import GCP_PROJECT_NUM
from dagster_gcp.gcs import GCSResource

# Create Definitions with resources
gcs_roswell = GCSResource(
    project=str(GCP_PROJECT_NUM),
    gcs_bucket="roswellbubbler_dev",
    gcs_prefix="observations",
)

defs = Definitions(
    assets=load_assets_from_modules([assets]),
    resources={"gcs_roswell": gcs_roswell}, 
)