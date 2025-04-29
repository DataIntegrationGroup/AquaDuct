import dagster as dg
import workflows.hydrovu as hydrovu #this import crashing, fix it. Check out the dockerfiles too to see how this file is invoked by dagster. ai!


modules = [hydrovu]
all_assets = dg.load_assets_from_modules([m.assets for m in modules])

definitions = dg.Definitions(
  assets=all_assets,
  resources={},
)