# ADK Text Summarization Agent

A text summarization AI agent built with Google Agent Development Kit (ADK) and Gemini, deployed on Cloud Run via Vertex AI.

---

## Project Structure

```
summarizer-agent/          ← repo root
├── .venv/                 ← virtual environment (never committed)
├── .gitignore
├── README.md
├── requirements.txt
└── summarizer_agent/      ← agent package
    ├── agent.py
    ├── __init__.py
    └── .env               ← never committed
```

---

## Prerequisites

- Python 3.12+
- [uv](https://astral.sh/uv) — fast Python package manager
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
- A Google Cloud project with billing enabled

---

## Setup

### 1. Authenticate with Google Cloud
```bash
gcloud auth login
gcloud config set account YOUR_GOOGLE_ACCOUNT_EMAIL
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default set-quota-project YOUR_PROJECT_ID
```

### 2. Create and activate virtual environment
```bash
uv venv --python 3.12
source .venv/bin/activate
```

### 3. Install dependencies
```bash
uv pip install -r requirements.txt
```

### 4. Configure environment variables
Create `summarizer_agent/.env` with the following:
```
PROJECT_ID=your-project-id
PROJECT_NUMBER=your-project-number
SA_NAME=summarizer-agent-sa
SERVICE_ACCOUNT=summarizer-agent-sa@your-project-id.iam.gserviceaccount.com
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=True
MODEL=gemini-2.5-flash
```

---

## Run Locally

```bash
source summarizer_agent/.env
adk run summarizer_agent
```

Or use the ADK web UI:
```bash
adk web
```
Then open http://localhost:8000 in your browser.

---

## Deploy to Cloud Run

### 1. Create a Service Account and grant Vertex AI access
```bash
source summarizer_agent/.env
gcloud iam service-accounts create ${SA_NAME} \
    --display-name="Service Account for Summarizer Agent"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/aiplatform.user"
```

### 2. Deploy using the ADK CLI
```bash
uvx --from google-adk \
  adk deploy cloud_run \
    --project=$PROJECT_ID \
    --region=us-central1 \
    --service_name=summarizer-agent \
    --with_ui \
    ./summarizer_agent \
    -- \
    --service-account=$SERVICE_ACCOUNT
```

### 3. Access the deployed agent
Once deployed, open the Cloud Run service URL in your browser to use the ADK web UI, or call it as an HTTP endpoint:
```bash
curl -X POST https://YOUR_CLOUD_RUN_URL/run \
  -H "Content-Type: application/json" \
  -d '{"message": "Summarize: Your text here..."}'
```

---

## Clean Up

```bash
gcloud run services delete summarizer-agent --region=us-central1 --quiet
gcloud artifacts repositories delete cloud-run-source-deploy --location=us-central1 --quiet
```