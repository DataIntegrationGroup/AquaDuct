# AquaDuct
New Mexico Water Data Initiative's data pipeline

Deployment steps:
- If no dagster vm exists yet, run `create_vm.sh`.
- Login to dagster vm as user 'deploy', using ssh agent forwarding (-A) `gcloud compute ssh deploy@dagster --ssh-flags="-A"`
- Clone the repo: `git clone git@github.com:DataIntegrationGroup/AquaDuct.git`
- Now deployment is set up. Anytime you want to push new code and restart the services, run `./deploy.sh` locally.
