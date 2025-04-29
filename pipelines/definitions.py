from dagster import Definitions
from dagster import load_assets_from_modules
from pipelines.workflows import hydrovu

modules = [hydrovu]
all_assets = load_assets_from_modules(modules)

defs = Definitions(assets=all_assets)