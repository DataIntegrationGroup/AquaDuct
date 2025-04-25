from dagster import asset, Definitions
 
@asset
def hello_world():
    print("Hello, world!")

@asset
def another_asset():
    print("asdf asdf asdf")

hydrovu_definitions = Definitions(
  assets=[hello_world, another_asset],
  resources={},
)