#!/bin/bash
set -euo pipefail

echo "Starting deployment..."

gcloud compute ssh deploy@dagster \
  --ssh-flag="-AT" \
  --command '
    [ -d AquaDuct ] &&
    cd AquaDuct &&
    git pull &&

    TMP_ENV=$(mktemp)
    cleanup() {
      echo "Cleaning up..."
      rm -f "$TMP_ENV"
    }
    trap cleanup EXIT

    echo "Fetching secrets..."
    SECRET_JSON=$(gcloud secrets versions access latest --secret=nmwdiproduction_dagster_psql)
    POSTGRES_USER=$(echo "$SECRET_JSON" | jq -r '.user')
    POSTGRES_PASSWORD=$(echo "$SECRET_JSON" | jq -r '.password')

    cat > "$TMP_ENV" <<EOF
    PG_USER=$PG_USER
    PG_PASS=$PG_PASS
    EOF

    sudo docker compose down --remove-orphans && 
    sudo docker compose --env-file "$TMP_ENV" up --build --force-recreate -d

    cleanup
  '

echo "Done deploying!"