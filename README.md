# 🛡️ StackGuardian — Troubleshooting Agent

StackGuardian is an AI-powered troubleshooting assistant that analyzes DevOps, CI/CD, Docker, Kubernetes, and Jenkins logs to automatically detect failures and provide root-cause analysis + recommended fixes.

Built with **Python (FastAPI)**, **OpenAI GPT-4.1**, **Streamlit UI**, and deployable on **AWS EC2**.

---

## 🚀 Features
- **AI Log Analysis**  
  Upload or paste log files (.txt or raw logs). The agent extracts patterns and produces:
  - Root cause summary  
  - Log category (CI/CD, Kubernetes, Docker, etc.)  
  - Risk level  
  - Step-by-step remediation

- **FastAPI Backend**  
  `/analyze` API endpoint processes logs and sends structured prompts to OpenAI.

- **Streamlit Frontend UI**  
  Clean, modern interface for DevOps engineers to paste logs and view instant results.

- **Fully Deployable on AWS EC2**  
  Clone → install → run backend + UI.

---

## 🧠 Tech Stack

### **Backend**
- Python 3
- FastAPI
- Uvicorn
- OpenAI API (GPT-4.1)

### **Frontend**
- Streamlit  
- Python (requests)

### **DevOps**
- Ubuntu EC2 Instance  
- Systemd optional for background service  
- Security groups for ports 8000 + 8501

---

## 📁 Project Structure

```
stackguardian-agent/
├── app/
│   ├── __init__.py
│   ├── agent.py             # AI logic + OpenAI structured output
│   ├── main.py              # FastAPI backend /analyze endpoint
│
├── ui/
│   ├── app.py               # Streamlit UI
│
├── test_logs/
│   ├── jenkins_invalid_branch.log
│
├── .env.example             # Sample environment file
├── requirements.txt         # Python dependencies
├── README.md
├── ROADMAP.md
```

---

## ⚙️ Local Setup (Start Here)

### 🔹 1. Clone the Repository
```bash
git clone https://github.com/keshvi-k/stackguardian-agent.git
cd stackguardian-agent
```

### 🔹 2. Create Virtual Environment
```bash
python3 -m venv venv
```

#### Activate it:

**macOS / Linux**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

---

### 🔹 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 🔹 4. Add OpenAI API Key
Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env`:

```
OPENAI_API_KEY=your_key_here
```

---

### 🔹 5. Run the Backend (FastAPI)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend available at:

```
http://localhost:8000/docs
```

---

### 🔹 6. Run the Frontend (Streamlit UI)
Open new terminal (with venv activated):

```bash
streamlit run ui/app.py --server.port 8501
```

UI available at:

```
http://localhost:8501
```

---

## ☁️ AWS EC2 Deployment (Ubuntu)

### 1. Launch EC2 Instance
- Ubuntu 22.04 or 24.04  
- Allow inbound:
  - **Port 22** (SSH)
  - **Port 8000** (backend)
  - **Port 8501** (UI)

### 2. SSH Into Instance
```bash
ssh -i "stackguardian-key.pem" ubuntu@<ec2-public-ip>
```

### 3. Install Python + Git
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y
```

### 4. Clone Repo
```bash
git clone https://github.com/keshvi-k/stackguardian-agent.git
cd stackguardian-agent
```

### 5. Create Venv & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 6. Start Backend
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
```

### 7. Start UI
```bash
streamlit run ui/app.py --server.port 8501 --server.address 0.0.0.0 &
```

### EC2 Public URLs:
```
http://<EC2-IP>:8000/docs      # backend
http://<EC2-IP>:8501           # frontend
```

---

## 📝 Sample Output (from AI)

```
{
  "log_type": "KUBERNETES",
  "category": "RESOURCE",
  "summary": "Kubernetes cannot pull the image 'nginx:latest' due to missing manifest.",
  "steps": [
    "Verify image exists in registry",
    "Try docker pull manually",
    "Check network or proxy issues",
    "Ensure imagePullSecrets are configured",
    "Specify a non-latest image tag"
  ]
}
```

---

## 🧭 Roadmap
- Multi-log comparison  
- Real-time log streaming agent  
- Multi-cloud deployments (AWS / GCP / Azure)  
- Slack & Teams integration  

---

## ❤️ Contributing
Pull requests welcome.

---

## 📄 License
MIT License.

