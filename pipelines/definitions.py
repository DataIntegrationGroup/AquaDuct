import dagster as dg
from workflows.hydrovu import assets as hydrovu_assets


modules = [hydrovu]
all_assets = dg.load_assets_from_modules([m.assets for m in modules]) #why does this have no module assets? it crashes. ai?

definitions = dg.Definitions(
  assets=all_assets,
  resources={},
)
