from sqlalchemy import Date, Index
from sqlalchemy.orm import Mapped
from model.base_model import Base

class TickerDailyData(Base):
    __tablename__ = "ticker_daily_data"

    ticker_symbol = Mapped[str]
    date = Mapped[Date]
    open = Mapped[float]
    high = Mapped[float]
    low = Mapped[float]
    close = Mapped[float]
    volume = Mapped[int]

    __table_args__ = (
        Index('idx_ticker_date', 'ticker_symbol', 'date'),
    )