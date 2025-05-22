from dagster import Definitions, load_assets_from_modules
from pipelines.workflows.cityofroswell import assets
from pipelines.utils.secrets import GCP_PROJECT_NUM
from dagster_gcp.gcs import GCSResource

defs = Definitions(
  assets=load_assets_from_modules([assets]),
  resources={
      "gcs": GCSResource(
          project=str(GCP_PROJECT_NUM),
          bucket="roswellbubbler_dev",
          prefix="observations"
      ),
  },
)