from dagster import Definitions
import pipelines.workflows.hydrovu.definitions as hydrovu_definitions
import pipelines.workflows.cityofroswell.definitions as cityofroswell_definitions
from pipelines.utils.resources import SensorThingsResource

shared_resources_def = Definitions(
    resources={
        "frost": SensorThingsResource(
            frost_url="http://localhost:8080/FROST-Server/v1.1"
        )
    }
)

defs = Definitions.merge(
    shared_resources_def,
    cityofroswell_definitions.defs,
    )