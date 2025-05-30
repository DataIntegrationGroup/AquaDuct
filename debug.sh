#!/usr/bin/env bash
set -euo pipefail

#This ugly hack allows us to have a dev and prod dagster.yaml.
#Dagster's cli doesn't allow us to specify one, so the workaround here is changing the name of our dagster.yaml so dagster can't find it.
#Dagster will then use its internal defaults rather than dagster.yaml.
mv dagster.yaml dagster.prod.yaml
cleanup() {
  echo "Cleaning up..."
  mv dagster.prod.yaml dagster.yaml
  docker compose -p frost-dev down
}
trap cleanup EXIT

docker compose -p frost-dev -f frost-compose.dev.yaml up -d #For quick startup (if frost not needed), comment this line out.
dagster dev -m pipelines.definitions
