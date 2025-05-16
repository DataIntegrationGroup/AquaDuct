#!/usr/bin/env bash
set -euo pipefail

echo "Starting deployment..."

gcloud compute ssh dagster \
  --ssh-flag="-AT" \
  --command '
    set -euo pipefail
    if [ -d AquaDuct ]; then
      cd AquaDuct && git pull
    else
      git clone git@github.com:DataIntegrationGroup/AquaDuct.git &&
      git checkout main &&
      cd AquaDuct
    fi

    TMP_ENV=$(mktemp)
    cleanup() {
      echo "Cleaning up..."
      rm -f "$TMP_ENV"
      sudo docker compose -p dagster down --remove-orphans
      sudo docker compose -p frost-dev down --remove-orphans
    }
    trap cleanup EXIT

    echo "Fetching secrets..."
    SECRET_JSON=$(gcloud secrets versions access latest --secret=nmwdiproduction_dagster_psql)
    PG_USER=$(echo "$SECRET_JSON" | jq -r '.user')
    PG_PASSWORD=$(echo "$SECRET_JSON" | jq -r '.password')

    (
      printf "PG_USER=$PG_USER\n"
      printf "PG_PASSWORD=$PG_PASSWORD\n"
    ) > $TMP_ENV

    sudo docker compose -p frost-dev down
    sudo docker compose -p frost-dev -f frost-compose.dev.yaml up -d #NOTE: this frost server is for development/testing.
    sudo docker compose -p dagster down --remove-orphans
    sudo docker compose -p dagster --env-file "$TMP_ENV" up --build --force-recreate -d
  '

echo "Done deploying!"