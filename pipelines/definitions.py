import dagster as dg
from pipelines.definitions import hydrovu


# Option 1: Load the modules directly
all_assets = dg.load_assets_from_modules([hydrovu.assets])

# Option 2 (alternative): If you want to keep your list approach
# modules = [hydrovu]
# all_assets = dg.load_assets_from_modules([m.assets for m in modules])

definitions = dg.Definitions(
  assets=all_assets,
  resources={},
)
