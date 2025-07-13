from fastapi import FastAPI
from contextlib import asynccontextmanager
from server.scripts.data_loading import run_data_loading
from server.router.ticker_router import router as ticker_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    await run_data_loading()
    yield


app = FastAPI(
    title="Financial Analysis API",
    description="API for financial data analysis and ticker information",
    version="1.0.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(ticker_router)


@app.get("/health")
def health_check():
    return {"Health Check": "Healthy!"}
