#!/bin/bash
set -euo pipefail

echo "Starting deployment..."

gcloud compute ssh deploy@dagster \
  --ssh-flag="-AT" \
  --command '
    [ -d AquaDuct ] &&
    (cd AquaDuct && git pull) &&
    (cd AquaDuct && sudo docker compose down --remove-orphans && sudo docker compose up --build --force-recreate -d)
  '

echo "Done deploying!"