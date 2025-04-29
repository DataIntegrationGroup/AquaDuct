import dagster as dg
from pipelines.definitions import hydrovu


modules = [hydrovu]
all_assets = dg.load_assets_from_modules([m.assets for m in modules])

definitions = dg.Definitions(
  assets=all_assets,
  resources={},
)
