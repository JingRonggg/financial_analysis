from sqlalchemy import Date, Index, String, Integer, Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from server.model.base_model import Base
from datetime import datetime
from typing import Optional


class TickerDailyData(Base):
    __tablename__ = "daily_ticker_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ticker_symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    open: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[int] = mapped_column(Integer, nullable=False)
    interval: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True, default="1d"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )

    __table_args__ = (
        Index("idx_ticker_date", "ticker_symbol", "date"),
        Index("idx_ticker_symbol", "ticker_symbol"),
        Index("idx_date", "date"),
    )

    def __repr__(self) -> str:
        return f"<TickerDailyData(id={self.id}, ticker={self.ticker_symbol}, date={self.date}, close={self.close})>"
