#!/bin/bash
set -euo pipefail


echo "Starting deployment..."

gcloud compute ssh deploy@dagster \
  --ssh-flag="-AT" \
  --command '[ -d AquaDuct ] && (cd AquaDuct && git pull)'

echo "Done deploying!"