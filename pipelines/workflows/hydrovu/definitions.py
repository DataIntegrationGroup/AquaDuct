from dagster import Definitions, load_assets_from_modules
from pipelines.workflows.hydrovu import assets

defs = Definitions(
  assets=load_assets_from_modules([assets])
)