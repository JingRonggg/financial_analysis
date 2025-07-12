from fastapi import FastAPI
from contextlib import asynccontextmanager
from server.scripts.data_loading import run_data_loading


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    await run_data_loading()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"Health Check": "Healthy!"}
