# Shared resoruces for pipelines
import dagster as dg
import frost_sta_client as fsc
from pydantic import Field

#Sensor Things API Resource
class SensorThingsResource(dg.ConfigurableResource):
    """
    Resource for interacting with SensorThings API.
    """
    frost_url: str = Field(
        default="http://localhost:8080/FROST-Server/v1.1",
        description="The base URL for the FROST SensorThings API."
    )

    def get_client(self) -> fsc.SensorThingsService:
        """
        Returns a SensorThings client configured with the provided FROST URL.
        """
        return fsc.SensorThingsService(self.frost_url)
    