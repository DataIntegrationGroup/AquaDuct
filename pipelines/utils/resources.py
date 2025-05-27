# Shared resoruces for pipelines
import dagster as dg
import frost_sta_client as fsc

#Sensor Things API Resource
class SensorThingsResource(dg.ConfigurableResource):
    """
    Resource for interacting with SensorThings API.
    """
    frost_url: str = dg.Field(
        str,
        description="The base URL for the FROST SensorThings API.",
        default_value="http://localhost:8080/FROST-Server/v1.1"
    )

    def get_client(self) -> fsc.SensorThingsService:
        """
        Returns a SensorThings client configured with the provided FROST URL.
        """
        return fsc.SensorThingsService(self.frost_url)
    