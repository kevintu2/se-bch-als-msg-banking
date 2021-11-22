# project-bch-als-msg-banking

Boston Children's Hospital ALS Message Banking Project(Double dipping audio editor)

## Frontend

`cd client`

### Run locally:

`npm install`

`npm start`

### To Deploy:

Push to `main` or create a PR to main to see the deployed website. CI/CD deploys to Firebase Hosting. The frontend can be accessible at [als-message-banking.web.app/](https://als-message-banking.web.app/)right now. 

## Backend

`cd backend`

### Run locally

`python3 -m venv env`

`source env/bin/activate`

`pip3 install -r requirements.txt`

`python3 app.py`

### To Deploy:

Backend is deployed onto GCP. After setting up an instance on GCP and authenticating through the platform, run the following commands to deply the backend API. 

```bash
docker build -t us-docker.pkg.dev/als-message-banking/docker/api-dev:latest .
docker push us-docker.pkg.dev/als-message-banking/docker/api-dev:latest
gcloud run deploy api-dev \
--image=us-docker.pkg.dev/als-message-banking/docker/api-dev:latest \
--platform=managed \
--region=us-central1 \
--project=als-message-banking
```
