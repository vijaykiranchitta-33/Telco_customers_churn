@echo off
SET PROJECT_ID=your-google-project-id
SET SERVICE_NAME=churn-prediction-api
SET REGION=us-central1

call gcloud builds submit --tag gcr.io/%PROJECT_ID%/%SERVICE_NAME% .

call gcloud run deploy %SERVICE_NAME% ^
  --image gcr.io/%PROJECT_ID%/%SERVICE_NAME% ^
  --platform managed ^
  --region %REGION% ^
  --allow-unauthenticated

pause