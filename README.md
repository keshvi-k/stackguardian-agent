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
