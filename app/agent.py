import json
import os

from typing import Dict, List

from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env (this is where your OPENAI_API_KEY is read)
load_dotenv()

# Create the client using your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are StackGuardian, an expert Dev & DevOps troubleshooter.

You analyze logs from:
- CI/CD tools: Jenkins, GitHub Actions, Bamboo
- Containers: Docker
- Orchestration: Kubernetes, OpenShift
- Application runtimes: Java Spring Boot, Node.js, .NET

Given a raw log:
1) Detect the log_type as one of: [CICD, DOCKER, KUBERNETES, APP, UNKNOWN].
2) Summarize the root cause in 2–3 concise sentences.
3) Classify the primary issue category as one of:
   [BUILD, RUNTIME, CONFIG, NETWORK, PERMISSION, RESOURCE, OTHER].
4) Provide 3–6 specific fix steps. Be practical and technical (commands, config hints, etc.).

You MUST return a JSON object with exactly these keys:
- log_type: string
- category: string
- summary: string
- steps: array of strings

Do not include any extra keys.
"""


def analyze_log(log: str) -> Dict:
    """
    Send the log to the LLM and get back a structured JSON result.

    NOTE: Calling this function WILL use the OpenAI API and incur a tiny cost per call.
    """
    if not log or not log.strip():
        return {
            "log_type": "UNKNOWN",
            "category": "OTHER",
            "summary": "No log content provided.",
            "steps": [
                "Provide a non-empty log snippet for analysis."
            ],
        }

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",  # you can change to another Chat Completions model if needed
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": log},
        ],
        response_format={"type": "json_object"},
    )

    # Because we requested JSON, the SDK parses it for us:
    
    result = json.loads(completion.choices[0].message.content)

    # ---- Normalize / sanitize the result a bit ----
    valid_log_types = {"CICD", "DOCKER", "KUBERNETES", "APP", "UNKNOWN"}
    valid_categories = {"BUILD", "RUNTIME", "CONFIG", "NETWORK", "PERMISSION", "RESOURCE", "OTHER"}

    log_type = str(result.get("log_type", "UNKNOWN")).upper()
    category = str(result.get("category", "OTHER")).upper()

    if log_type not in valid_log_types:
        log_type = "UNKNOWN"
    if category not in valid_categories:
        category = "OTHER"

    steps = result.get("steps", [])
    if isinstance(steps, str):
        steps = [steps]
    elif not isinstance(steps, list):
        steps = [str(steps)]

    normalized = {
        "log_type": log_type,
        "category": category,
        "summary": str(result.get("summary", "")),
        "steps": [str(s).strip() for s in steps if str(s).strip()],
    }

    # Make sure we always have at least one step
    if not normalized["steps"]:
        normalized["steps"] = ["No specific steps generated. Review the log manually."]

    return normalized
