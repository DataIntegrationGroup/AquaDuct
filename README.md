# AquaDuct
New Mexico Water Data Initiative's data pipeline

### Connecting to Dagster UI
- run `gcloud compute ssh dagster -- -L 3000:localhost:3000 -N`

### Deployment steps:
- If no dagster vm exists yet, run `create_vm.sh`.
- Login to dagster vm as user 'deploy', using ssh agent forwarding (-A) `gcloud compute ssh deploy@dagster --ssh-flags="-A"`
- Clone the repo: `git clone git@github.com:DataIntegrationGroup/AquaDuct.git`
- Run `./deploy.sh` locally.