import dagster as dg
from dagster import asset
 
@asset
def hello_world():
    print("Hello, world!")

@asset
def another_asset():
    print("asdf asdf asdf")

hydrovu_definitions = dg.Definitions(
  assets=[hello_world, another_asset],
  resources={},
)