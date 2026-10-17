from fastapi import FastAPI

app = FastAPI(
    title="Agentic QA Platform",
    description="AI-assisted Quality Engineering Platform",
    version="0.1.0"
)

@app.get("/")
def root():
    return{
        "message" : "Welcome to the Agentic QA Platform"
    }

@app.get("/health")
def health_check():
    return{
        "status" : "healthy",
        "service" : "agentic-qa-platform"
    }