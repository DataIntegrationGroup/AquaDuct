#!/bin/bash
set -euo pipefail

echo "Starting deployment..."

gcloud compute ssh deploy@dagster \
  --ssh-flag="-AT" \
  --command '
    [ -d AquaDuct ] &&
    (cd AquaDuct && git pull) &&
    (cd AquaDuct/dagster_deployment && sudo docker compose up -d)
  '

echo "Done deploying!"