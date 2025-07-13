from pydantic import BaseModel, Field
from datetime import date as Date, datetime as DateTime
from typing import List, Optional


class TickerDataResponse(BaseModel):
    """Response model for ticker data."""

    id: int
    ticker_symbol: str = Field(..., description="Stock ticker symbol")
    date: Date = Field(..., description="Trading date")
    open: float = Field(..., description="Opening price")
    high: float = Field(..., description="Highest price")
    low: float = Field(..., description="Lowest price")
    close: float = Field(..., description="Closing price")
    volume: int = Field(..., description="Trading volume")
    interval: Optional[str] = Field(default="1d", description="Time interval")
    created_at: DateTime = Field(..., description="Record creation timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "ticker_symbol": "AAPL",
                "date": "2024-01-15",
                "open": 185.50,
                "high": 188.75,
                "low": 184.25,
                "close": 187.20,
                "volume": 50000000,
                "interval": "1d",
                "created_at": "2024-01-15T10:00:00",
            }
        }


class TickerDataListResponse(BaseModel):
    """Response model for list of ticker data."""

    ticker_symbol: str = Field(..., description="Stock ticker symbol")
    count: int = Field(..., description="Number of records returned")
    data: List[TickerDataResponse] = Field(..., description="List of ticker data")

    class Config:
        json_schema_extra = {
            "example": {
                "ticker_symbol": "AAPL",
                "count": 2,
                "data": [
                    {
                        "id": 1,
                        "ticker_symbol": "AAPL",
                        "date": "2024-01-15",
                        "open": 185.50,
                        "high": 188.75,
                        "low": 184.25,
                        "close": 187.20,
                        "volume": 50000000,
                        "interval": "1d",
                        "created_at": "2024-01-15T10:00:00",
                    }
                ],
            }
        }


class PriceStatisticsResponse(BaseModel):
    """Response model for price statistics."""

    ticker_symbol: str = Field(..., description="Stock ticker symbol")
    days: int = Field(..., description="Number of days analyzed")
    avg_close: float = Field(..., description="Average closing price")
    max_high: float = Field(..., description="Maximum high price")
    min_low: float = Field(..., description="Minimum low price")
    avg_volume: float = Field(..., description="Average trading volume")
    latest_close: float = Field(..., description="Most recent closing price")
    price_change: float = Field(
        ..., description="Price change percentage over the period"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "ticker_symbol": "AAPL",
                "days": 30,
                "avg_close": 186.25,
                "max_high": 195.50,
                "min_low": 175.80,
                "avg_volume": 52000000.0,
                "latest_close": 187.20,
                "price_change": 2.35,
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(
        default=None, description="Detailed error information"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Ticker not found",
                "detail": "No data found for ticker symbol: INVALID",
            }
        }
