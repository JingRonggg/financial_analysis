from typing import List, Optional, Dict, Any
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, desc, asc
from server.repository.base_repository import BaseRepository
from server.repository.database import get_db_session
from server.model.ticker import TickerDailyData


class TickerRepository(BaseRepository[TickerDailyData]):
    """Repository for TickerDailyData with CRUD operations."""

    def __init__(self, db_session: Optional[Session] = None):
        if db_session is None:
            db_session = get_db_session()
        super().__init__(db_session, TickerDailyData)

    def get_by_ticker_and_date(
        self, ticker_symbol: str, date_val: date
    ) -> Optional[TickerDailyData]:
        """Get ticker data by symbol and date."""
        try:
            stmt = select(TickerDailyData).where(
                and_(
                    TickerDailyData.ticker_symbol == ticker_symbol,
                    TickerDailyData.date == date_val,
                )
            )
            result = self.db_session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise RuntimeError(
                f"Error retrieving ticker data for {ticker_symbol} on {date_val}: {str(e)}"
            )

    def get_by_ticker_symbol(
        self, ticker_symbol: str, limit: Optional[int] = None
    ) -> List[TickerDailyData]:
        """Get all data for a specific ticker symbol."""
        try:
            stmt = (
                select(TickerDailyData)
                .where(TickerDailyData.ticker_symbol == ticker_symbol)
                .order_by(desc(TickerDailyData.date))
            )

            if limit:
                stmt = stmt.limit(limit)

            result = self.db_session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RuntimeError(
                f"Error retrieving data for ticker {ticker_symbol}: {str(e)}"
            )

    def get_date_range(
        self, ticker_symbol: str, start_date: date, end_date: date
    ) -> List[TickerDailyData]:
        """Get ticker data within a date range."""
        try:
            stmt = (
                select(TickerDailyData)
                .where(
                    and_(
                        TickerDailyData.ticker_symbol == ticker_symbol,
                        TickerDailyData.date >= start_date,
                        TickerDailyData.date <= end_date,
                    )
                )
                .order_by(asc(TickerDailyData.date))
            )

            result = self.db_session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RuntimeError(f"Error retrieving ticker data for date range: {str(e)}")

    def get_latest_by_ticker(self, ticker_symbol: str) -> Optional[TickerDailyData]:
        """Get the most recent data for a ticker symbol."""
        try:
            stmt = (
                select(TickerDailyData)
                .where(TickerDailyData.ticker_symbol == ticker_symbol)
                .order_by(desc(TickerDailyData.date))
                .limit(1)
            )

            result = self.db_session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise RuntimeError(
                f"Error retrieving latest data for ticker {ticker_symbol}: {str(e)}"
            )

    def get_all_tickers(self) -> List[str]:
        """Get all unique ticker symbols."""
        try:
            stmt = select(TickerDailyData.ticker_symbol).distinct()
            result = self.db_session.execute(stmt)
            return [row[0] for row in result.fetchall()]
        except Exception as e:
            raise RuntimeError(f"Error retrieving all ticker symbols: {str(e)}")

    def create_ticker_data(self, ticker_data: Dict[str, Any]) -> TickerDailyData:
        """Create new ticker data entry."""
        try:
            # Add created_at if not provided
            if "created_at" not in ticker_data:
                ticker_data["created_at"] = datetime.now()

            entity = TickerDailyData(**ticker_data)
            return self.create(entity)
        except Exception as e:
            raise RuntimeError(f"Error creating ticker data: {str(e)}")

    def bulk_create(
        self, ticker_data_list: List[Dict[str, Any]]
    ) -> List[TickerDailyData]:
        """Create multiple ticker data entries in a single transaction."""
        try:
            entities = []
            for data in ticker_data_list:
                if "created_at" not in data:
                    data["created_at"] = datetime.now()
                entities.append(TickerDailyData(**data))

            self.db_session.add_all(entities)
            self.db_session.commit()

            # Refresh all entities to get their IDs
            for entity in entities:
                self.db_session.refresh(entity)

            return entities
        except Exception as e:
            self.db_session.rollback()
            raise RuntimeError(f"Error bulk creating ticker data: {str(e)}")

    def update_ticker_data(
        self, ticker_id: int, update_data: Dict[str, Any]
    ) -> Optional[TickerDailyData]:
        """Update ticker data by ID."""
        return self.update(ticker_id, update_data)

    def delete_ticker_data(self, ticker_id: int) -> bool:
        """Delete ticker data by ID."""
        return self.delete(ticker_id)

    def delete_by_ticker_and_date(self, ticker_symbol: str, date_val: date) -> bool:
        """Delete ticker data by symbol and date."""
        try:
            ticker_data = self.get_by_ticker_and_date(ticker_symbol, date_val)
            if ticker_data:
                return self.delete(ticker_data.id)
            return False
        except Exception as e:
            raise RuntimeError(
                f"Error deleting ticker data for {ticker_symbol} on {date_val}: {str(e)}"
            )

    def get_price_statistics(
        self, ticker_symbol: str, days: int = 30
    ) -> Optional[Dict[str, float]]:
        """Get price statistics for a ticker over the last N days."""
        try:
            stmt = (
                select(TickerDailyData)
                .where(TickerDailyData.ticker_symbol == ticker_symbol)
                .order_by(desc(TickerDailyData.date))
                .limit(days)
            )

            result = self.db_session.execute(stmt)
            data = result.scalars().all()

            if not data:
                return None

            closes = [d.close for d in data]
            highs = [d.high for d in data]
            lows = [d.low for d in data]
            volumes = [d.volume for d in data]

            return {
                "avg_close": sum(closes) / len(closes),
                "max_high": max(highs),
                "min_low": min(lows),
                "avg_volume": sum(volumes) / len(volumes),
                "latest_close": closes[0] if closes else 0,
                "price_change": (
                    (closes[0] - closes[-1]) / closes[-1] * 100
                    if len(closes) > 1
                    else 0
                ),
            }
        except Exception as e:
            raise RuntimeError(
                f"Error calculating price statistics for {ticker_symbol}: {str(e)}"
            )


def get_ticker_repository(db_session: Optional[Session] = None) -> TickerRepository:
    """Get a TickerRepository instance."""
    return TickerRepository(db_session)
