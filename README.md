# project-bch-als-msg-banking

Boston Children's Hospital ALS Message Banking Project (Double Dipping Audio Editor)

Speech impairment is common with patience with ALS diease. ALS Message Banking Project aims preserve their voice and assisst them with their needs.
The platform allows the user to create account and login to their own dashboard, where they can upload audio files and retrieve audio files
securly. The overarching goal will be to have these audio files be processed and filtered to enhance the sound quality and be able to reuse parts of the audio clips to produce new "voice" for the user.

## Technical Archtecture

## Frontend

`cd client`

### Run Frontend Locally

`npm install`

`npm start`

### To Deploy Frontend

Push to `main` or create a PR to main to see the deployed website. CI/CD deploys to Firebase Hosting. The frontend is accessible at [als-message-banking.web.app/](https://als-message-banking.web.app/)right now.

## Backend

`cd backend`

### Run Backend Locally

- Setup GOOGLE_APPLICATION_CREDENTIALS as described here - <https://cloud.google.com/docs/authentication/getting-started>

```bash
docker build -t als-backend .
docker run als-backend
```

### To Deploy Backend

Backend is deployed to GCP. After authenticating docker to push to the private docker repository, run the following commands to deploy the API.

```bash
docker build -t us-docker.pkg.dev/als-message-banking/docker/api-dev:latest .
docker push us-docker.pkg.dev/als-message-banking/docker/api-dev:latest
gcloud run deploy api-dev \
--image=us-docker.pkg.dev/als-message-banking/docker/api-dev:latest \
--platform=managed \
--region=us-central1 \
--project=als-message-banking
```
