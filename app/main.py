from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .agent import analyze_log


class LogRequest(BaseModel):
    log: str


app = FastAPI(
    title="StackGuardian – Troubleshooting Agent",
    version="0.1.0",
    description="Analyze Dev/DevOps logs and get structured root cause analysis + fix steps.",
)


@app.get("/")
def root():
    return {"message": "StackGuardian API is running. POST a log to /analyze to begin."}


@app.post("/analyze")
def analyze(req: LogRequest):
    """
    Accepts a raw log string, returns structured analysis.
    """
    try:
        result = analyze_log(req.log)
        return result
    except Exception as e:
        # This will print in the terminal and also show up in the API response
        print("Error in /analyze:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))
