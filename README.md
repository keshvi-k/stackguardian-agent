# StackGuardian – Troubleshooting Agent

An AI-powered assistant that helps DevOps engineers and developers quickly **understand, triage, and fix** failures in CI/CD, Docker, Kubernetes, and application logs.

StackGuardian takes raw Jenkins/Docker/K8s/app logs, sends them to an OpenAI model, and returns a **structured root-cause analysis** plus concrete remediation steps.

---

## Key Features

- **Log understanding, not just search**
  - Paste messy, multiline logs (Jenkins pipeline, Docker, K8s, app logs).
  - The agent detects error patterns and summarizes what actually went wrong.

- **Structured, actionable output**
  - Returns a JSON object with:
    - `log_type` – e.g., `CICD`, `KUBERNETES`, `DOCKER`, `APP`
    - `category` – e.g., `CONFIG`, `NETWORK`, `RUNTIME`
    - `summary` – one-paragraph root cause explanation
    - `steps` – ordered remediation checklist for engineers

- **FastAPI backend API**
  - `/` – health/metadata endpoint  
  - `/analyze` – accepts structured JSON `{ "log": "…" }`  
  - Optional `/analyze/raw` (if enabled) for raw pasted logs.

- **Streamlit web UI**
  - Paste logs in a text area, click **“Analyze Log”**, and see:
    - Human-readable explanation
    - Risk/impact
    - Recommended fix steps

- **Cloud-ready**
  - Built and tested on an **Ubuntu AWS EC2** instance.
  - Backend (FastAPI) + UI (Streamlit) run on the same host.
  - Easy to put behind Nginx or an ALB later.

---

## Tech Stack

**Language**

- Python 3.10+

**Backend**

- [FastAPI](https://fastapi.tiangolo.com/) – REST API for log analysis  
- [Uvicorn](https://www.uvicorn.org/) – ASGI server  
- [Pydantic](https://docs.pydantic.dev/) – request/response models  

**AI / LLM**

- [OpenAI Python SDK](https://github.com/openai/openai-python)  
- Model: `gpt-4.1-mini` (via the new **Responses API**)

**Frontend / UI**

- [Streamlit](https://streamlit.io/) – lightweight UI for pasting logs and viewing analysis

**Other**

- `requests` – UI → backend HTTP calls  
- `.env` management for secrets (`OPENAI_API_KEY`)

**Infra (deployment example)**

- AWS EC2 (Ubuntu 24.04 LTS)
- Security group with open ports for:
  - `22` (SSH)
  - `8000` (FastAPI)
  - `8501` (Streamlit)

---

## Project Structure

```text
stackguardian-agent/
├── app/
│   ├── __init__.py
│   ├── agent.py        # Core AI logic: calls OpenAI and structures the response
│   └── main.py         # FastAPI app + /analyze endpoints
│
├── ui/
│   └── app.py          # Streamlit UI: paste logs and call backend
│
├── test_logs/
│   └── jenkins_invalid_branch.log  # Sample failing Jenkins pipeline log
│
├── .env.example        # Template for environment variables
├── requirements.txt    # Python dependencies
├── README.md           # You are here 
└── ROADMAP.md          # Future enhancements and ideas
⚙️ Local Setup
1. Prerequisites

Python 3.10+

pip

An OpenAI API key with access to gpt-4.1-mini

2. Clone the repository
git clone https://github.com/keshvi-k/stackguardian-agent.git
cd stackguardian-agent

3. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # macOS / Linux
# OR
venv\Scripts\activate         # Windows (PowerShell / CMD)

4. Install dependencies
pip install -r requirements.txt

5. Configure environment variables

Create a .env file in the project root, based on .env.example:

cp .env.example .env


Then edit .env and set at least:

OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4.1-mini
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000


(For local development you can keep BACKEND_HOST as 0.0.0.0 and call http://localhost:8000.)

🚀 Running the App Locally
1. Start the FastAPI backend

From the project root (with the virtualenv activated):

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


You can now open:

FastAPI docs: http://localhost:8000/docs

Health endpoint: GET http://localhost:8000/

2. Start the Streamlit UI

In a second terminal (same virtualenv):

streamlit run ui/app.py


By default, Streamlit will run at:

http://localhost:8501

The UI will send requests to http://localhost:8000/analyze (or to the URL configured in the UI code / env variable).

🧪 Example Usage

Open http://localhost:8501 in your browser.

Paste a failing Jenkins log, e.g.:

Branch: develop
[Pipeline] error
ERROR: Invalid branch name format: null
Build step 'Execute shell' marked build as failure
Finished: FAILURE


Click “Analyze Log”.

Backend response (simplified):

{
  "log_type": "CICD",
  "category": "CONFIG",
  "summary": "The Jenkins pipeline failed early due to an invalid or null branch name, causing downstream stages to be skipped.",
  "steps": [
    "Verify the branch name variable is correctly set and passed into the pipeline.",
    "Add logging or echo statements to confirm the branch value early in the pipeline.",
    "Validate that the SCM/checkout step retrieves a valid branch and not null.",
    "Update branch naming rules and enforce them in the pipeline configuration."
  ]
}


The Streamlit UI renders this in a clean, human-friendly way.

☁️ AWS EC2 Deployment (High-Level)

These are the same steps we used to get StackGuardian running on an Ubuntu EC2 instance:

Create EC2 instance

AMI: Ubuntu 24.04 LTS

Instance type: t3.small / t3.medium (or similar)

Attach a security group that allows:

22 (SSH) – your IP

8000 (FastAPI)

8501 (Streamlit)

SSH into the instance

ssh -i stackguardian-key.pem ubuntu@<EC2_PUBLIC_IP>


Install Python and Git

sudo apt update
sudo apt install -y python3 python3-venv python3-pip git


Clone repo & set up environment

git clone https://github.com/keshvi-k/stackguardian-agent.git
cd stackguardian-agent

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
nano .env      # paste OPENAI_API_KEY etc.


Run backend and UI (using screen or tmux)

Backend:

screen -S backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
# Ctrl+A, D to detach


UI:

screen -S ui
streamlit run ui/app.py --server.address=0.0.0.0 --server.port=8501
# Ctrl+A, D to detach


Access from browser

Backend docs: http://<EC2_PUBLIC_IP>:8000/docs

Streamlit UI: http://<EC2_PUBLIC_IP>:8501

For production, you can front this with Nginx and HTTPS, or move to a containerized setup (Docker + ECS/EKS).
