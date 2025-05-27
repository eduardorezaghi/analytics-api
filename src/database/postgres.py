import asyncio
from curses import raw
from functools import lru_cache
from io import StringIO
from typing import Literal

import pandas as pd
import sqlalchemy
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.conf import settings
from src.models.base import Base
from src.models.program_prediction import ProgramPrediction


@lru_cache
def get_sync_engine() -> sqlalchemy.engine.Engine:
    sync_engine = create_engine(str(settings.database_url))
    return sync_engine

@lru_cache
def get_async_engine() -> sqlalchemy.engine.Engine:
    async_engine = create_async_engine(str(settings.database_url))
    return async_engine

def get_async_session() -> AsyncSession:
    """
    Get a new async database session.
    """
    async_engine = get_async_engine()
    AsyncSessionLocal = async_sessionmaker(
        bind=async_engine, expire_on_commit=False, class_=AsyncSession
    )
    return AsyncSessionLocal()

def init_db():
    """
    Create the program_predictions table in the database (if not exists).
    """
    Base.metadata.create_all(bind=get_sync_engine())


async def _init_db_async():
    async with get_async_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db_session() -> AsyncSession:
    """
    Get a new async database session.
    """
    async with get_async_session() as session:
        yield session


def write_program_predictions(df: pd.DataFrame) -> None:
    """
    Bulk load DataFrame into program_predictions using PostgreSQL COPY for performance.
    Expects df columns: ['signal', 'program_code', 'weekday', 'available_time', 'predicted_audience']
    """
    init_db()
    sync_engine = get_sync_engine()
    raw_conn = sync_engine.connect().connection
    try:
        with raw_conn.cursor() as cur:
            with cur.copy(
                f"COPY {ProgramPrediction.__tablename__} ({', '.join(df.columns)}) FROM STDIN WITH CSV HEADER"
            ) as copy:
                df.to_csv(copy, index=False, header=True)

            raw_conn.commit()
    finally:
        raw_conn.close()


async def get_data_by_program_code(
    program_code: str,
    exhibition_date: str | None = None,
    db: AsyncSession | None = None,
) -> list[ProgramPrediction]:
    """
    Filter and aggregate program predictions by program_code (async).
    """
    session = db or get_async_session()
    async with session as session:
        query = (
            sqlalchemy.select(
                ProgramPrediction.signal,
                ProgramPrediction.program_code,
                ProgramPrediction.weekday,
                sqlalchemy.func.sum(ProgramPrediction.available_time).label(
                    "total_available_time"
                ),
                sqlalchemy.func.avg(ProgramPrediction.predicted_audience).label(
                    "avg_predicted_audience"
                ),
            )
            .where(ProgramPrediction.program_code == program_code)
            .group_by(
                ProgramPrediction.signal,
                ProgramPrediction.program_code,
                ProgramPrediction.weekday,
            )
        )
        if exhibition_date:
            query = query.where(ProgramPrediction.exhibition_date == exhibition_date)
        result = await session.execute(query)
        return result.all()


async def get_data_by_period(
    program_code: str, start_date: str, end_date: str, db: AsyncSession | None = None
) -> list[ProgramPrediction]:
    """
    Retrieve program predictions for a specific period by program code (async).
    """
    session = db or get_async_session()
    async with session as session:
        query = (
            sqlalchemy.select(
                ProgramPrediction.signal,
                ProgramPrediction.program_code,
                ProgramPrediction.weekday,
                sqlalchemy.func.sum(ProgramPrediction.available_time).label(
                    "total_available_time"
                ),
                sqlalchemy.func.avg(ProgramPrediction.predicted_audience).label(
                    "avg_predicted_audience"
                ),
            )
            .where(
                ProgramPrediction.program_code == program_code,
                ProgramPrediction.exhibition_date >= start_date,
                ProgramPrediction.exhibition_date <= end_date,
            )
            .group_by(
                ProgramPrediction.signal,
                ProgramPrediction.program_code,
                ProgramPrediction.weekday,
            )
        )
        result = await session.execute(query)
        return result.all()
