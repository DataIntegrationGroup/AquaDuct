from dagster import Definitions
import pipelines.workflows.hydrovu.definitions as hydrovu_definitions
import pipelines.workflows.cityofroswell.definitions as cityofroswell_definitions

defs = Definitions.merge(hydrovu_definitions.defs, cityofroswell_definitions.defs)