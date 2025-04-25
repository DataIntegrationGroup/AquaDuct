import dagster as dg
from dagster import asset
 
@asset
def hello_world():
    print("Hello, world!")

hydrovu_definitions = dg.Definitions(
  assets=[hello_world],
  resources={},
)