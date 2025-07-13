from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ticker_router)


@app.get("/health")
def health_check():
    return {"Health Check": "Healthy!"}
