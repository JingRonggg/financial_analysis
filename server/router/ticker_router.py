from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional, List
from server.schemas.ticker_schemas import (
    TickerDataResponse,
    TickerDataListResponse,
)
from server.repository.ticker_repository import get_ticker_repository
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/ticker", tags=["ticker"])


@router.get(
    "/{ticker_symbol}",
    response_model=TickerDataListResponse,
    summary="Get ticker data by symbol",
    description="Retrieve all ticker data for a specific symbol with optional limit",
)
async def get_ticker_data(
    ticker_symbol: str = Path(
        ..., description="Stock ticker symbol (e.g., AAPL)", min_length=1, max_length=20
    ),
):
    """
    Get ticker data by symbol.

    - **ticker_symbol**: Stock ticker symbol (e.g., AAPL, GOOGL)

    Returns the most recent data first.
    """
    try:
        ticker_repo = get_ticker_repository()
        ticker_data = ticker_repo.get_by_ticker_symbol(ticker_symbol.upper())

        if not ticker_data:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for ticker symbol: {ticker_symbol.upper()}",
            )

        response_data = [
            TickerDataResponse.model_validate(data) for data in ticker_data
        ]

        return TickerDataListResponse(
            ticker_symbol=ticker_symbol.upper(),
            count=len(response_data),
            data=response_data,
        )

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get(
    "/",
    response_model=List[str],
    summary="Get all ticker symbols",
    description="Retrieve all available ticker symbols in the database",
)
async def get_all_ticker_symbols():
    """
    Get all available ticker symbols.

    Returns a list of all unique ticker symbols available in the database.
    """
    try:
        ticker_repo = get_ticker_repository()
        ticker_symbols = ticker_repo.get_all_tickers()

        if not ticker_symbols:
            raise HTTPException(
                status_code=404, detail="No ticker symbols found in the database"
            )

        return sorted(ticker_symbols)

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
