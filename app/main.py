from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

from .agent import analyze_log


class LogRequest(BaseModel):
    log: str


app = FastAPI(
    title="StackGuardian  Troubleshooting Agent",
    version="0.1.0",
    description=(
        "Analyze Dev/DevOps logs (CI/CD, Docker, Kubernetes, App runtime) "
        "and get structured root-cause analysis + fix steps."
    ),
)


@app.get("/")
def root():
    return {
        "message": "StackGuardian API is running. Use POST /analyze or POST /analyze/raw."
    }


def _sanitize_log(raw: str) -> str:
    """
    Normalize pasted logs so the model gets a clean string.
    """
    if not raw:
        return ""
    return (
        raw.replace("\r", "")      # fix newlines
           .replace("\t", "    ")  # replace tabs
           .strip()
    )


@app.post("/analyze")
def analyze(req: LogRequest):
    """
    JSON input (Swagger).
    """
    try:
        cleaned_log = _sanitize_log(req.log)

        if not cleaned_log:
            return {
                "log_type": "UNKNOWN",
                "category": "OTHER",
                "summary": "Empty log provided.",
                "steps": ["Provide a log first."],
            }

        return analyze_log(cleaned_log)

    except Exception as e:
        print("Error:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/raw")
def analyze_raw(
    log: str = Body(..., media_type="text/plain", description="Paste raw logs (no JSON required).")
):
    """
    Raw text input (Postman / plaintext).
    """
    try:
        cleaned_log = _sanitize_log(log)

        if not cleaned_log:
            return {
                "log_type": "UNKNOWN",
                "category": "OTHER",
                "summary": "Empty log provided.",
                "steps": ["Provide a log first."],
            }

        return analyze_log(cleaned_log)

    except Exception as e:
        print("Error:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))
