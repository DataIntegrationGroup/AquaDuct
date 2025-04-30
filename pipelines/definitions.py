from dagster import Definitions
import pipelines.workflows.hydrovu.definitions as hydrovu_definitions

defs = Definitions.merge(hydrovu_definitions.defs)