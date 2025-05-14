#!/usr/bin/env bash
set -euo pipefail

#This allows us to have a dev and prod dagster.yaml.
#Dagster's cli doesn't allow us to specify one, so this is the workaround.
mv dagster.yaml dagster.prod.yaml
cleanup() {
  echo "Cleaning up..."
  mv dagster.prod.yaml dagster.yaml
}
trap cleanup EXIT

dagster dev -m pipelines.definitions

cleanup