from io import StringIO
from typing import Literal

import pandas as pd
import sqlalchemy
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.conf import settings
from src.models.base import Base
from src.models.program_prediction import ProgramPrediction

engine = create_engine(str(settings.database_url))
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """
    Create the program_predictions table in the database (if not exists).
    """
    Base.metadata.create_all(bind=engine)


def get_db_session() -> Session:
    """
    Get a new database session.
    """
    db = SessionLocal()
    try:
        with db.begin():
            yield db
    finally:
        db.close()


def write_program_predictions(df: pd.DataFrame) -> None:
    """
    Bulk load DataFrame into program_predictions using PostgreSQL COPY for performance.

    Expects df columns: ['signal', 'program_code', 'weekday', 'available_time', 'predicted_audience']
    """
    init_db()

    raw_conn = engine.raw_connection()
    try:
        with raw_conn.cursor() as cur:
            buffer = StringIO()
            df.to_csv(buffer, index=False, header=True)
            buffer.seek(0)
            cur.copy_expert(
                sql=f"COPY {ProgramPrediction.__tablename__} ({', '.join(df.columns)}) FROM STDIN WITH CSV HEADER",
                file=buffer,
            )
        raw_conn.commit()
    finally:
        raw_conn.close()


def get_data_by_program_code(
    program_code: str,
    exhibition_date: str | None = None,
    db: Session | None = None,
) -> list[ProgramPrediction]:
    """
    Filter and aggregate program predictions by program_code.
    """
    session = db or SessionLocal()
    try:
        query = session.query(ProgramPrediction).filter(
            ProgramPrediction.program_code == program_code
        )
        if exhibition_date:
            # If exhibition_date is provided, filter by it
            query = query.filter(ProgramPrediction.exhibition_date == exhibition_date)
        # Group by program_code and weekday, and aggregate available_time and predicted_audience
        query = query.with_entities(
            ProgramPrediction.signal,
            ProgramPrediction.program_code,
            ProgramPrediction.weekday,
            sqlalchemy.func.sum(ProgramPrediction.available_time).label(
                "total_available_time"
            ),
            sqlalchemy.func.avg(ProgramPrediction.predicted_audience).label(
                "avg_predicted_audience"
            ),
        ).group_by(
            ProgramPrediction.signal,
            ProgramPrediction.program_code,
            ProgramPrediction.weekday,
        )
        # Execute the query and return results
        return query.all()
    finally:
        session.close()


def get_data_by_period(
    program_code: str, start_date: str, end_date: str, db: Session | None = None
) -> list[ProgramPrediction]:
    """
    Retrieve program predictions for a specific period by program code.
    """
    session = db or SessionLocal()
    try:
        query = session.query(ProgramPrediction).filter(
            ProgramPrediction.program_code == program_code,
            ProgramPrediction.exhibition_date >= start_date,
            ProgramPrediction.exhibition_date <= end_date,
        )
        # Group by program_code and weekday, and aggregate available_time and predicted_audience
        query = query.with_entities(
            ProgramPrediction.signal,
            ProgramPrediction.program_code,
            ProgramPrediction.weekday,
            sqlalchemy.func.sum(ProgramPrediction.available_time).label(
                "total_available_time"
            ),
            sqlalchemy.func.avg(ProgramPrediction.predicted_audience).label(
                "avg_predicted_audience"
            ),
        ).group_by(
            ProgramPrediction.signal,
            ProgramPrediction.program_code,
            ProgramPrediction.weekday,
        )
        # Execute the query and return results
        return query.all()
    finally:
        session.close()
