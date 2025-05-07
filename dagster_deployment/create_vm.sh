#!/bin/bash
set -euo pipefail

echo "Creating vm..."

gcloud compute instances create dagster \
    --project=waterdatainitiative-271000 \
    --zone=us-west3-a \
    --machine-type=e2-small \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=dagster@waterdatainitiative-271000.iam.gserviceaccount.com \
    --scopes=cloud-platform \
    --create-disk=auto-delete=yes,boot=yes,device-name=dagster,disk-resource-policy=projects/waterdatainitiative-271000/regions/us-west3/resourcePolicies/default-schedule-1,image=projects/ubuntu-os-cloud/global/images/ubuntu-minimal-2504-plucky-amd64-v20250415,mode=rw,size=10,type=pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ec-src=vm_add-gcloud \
    --reservation-affinity=any

gcloud compute ssh dagster --ssh-flag="-AT" --command='
  sudo apt update &&
  sudo apt install -y git curl unzip build-essential
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh ./get-docker.sh
  rm ./get-docker.sh
'

echo "Done creating vm!"