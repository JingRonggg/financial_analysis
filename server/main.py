from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"Health Check": "Healthy!"}