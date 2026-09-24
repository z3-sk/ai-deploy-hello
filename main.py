from fastapi import FastAPI

app = FastAPI(title="AI Deploy Service")

@app.get("/")
def read_root():
    return {"status": "success", "message": "Hello AI Deploy API!"}

@app.get("/health")
def health_check():
    return {"status": "ok", "gpu": "available", "service": "running"}