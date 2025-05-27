import datetime
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .base import Base

class ProgramPrediction(Base):
    __tablename__ = "program_data"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    signal: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    program_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    weekday: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    exhibition_date: Mapped[datetime.datetime] = mapped_column(nullable=True, index=True)
    available_time: Mapped[int] = mapped_column(Integer, nullable=False)
    predicted_audience: Mapped[float] = mapped_column(Float, nullable=True)
