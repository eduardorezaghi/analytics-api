import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI
from fastapi.responses import JSONResponse

from src.api.exceptions import BadRequestException
from src.api.schemas import ProgramPrediction
from src.api.schemas.requests import (
    ProgramPredictionCodeRequest,
    ProgramPredictionPeriodRequest,
)
from src.api.schemas.responses import ProgramPredictionResponse
from src.database.postgres import SessionLocal, get_db_session

app = FastAPI()

router = APIRouter(
    prefix="/analytics",
)


@app.exception_handler(BadRequestException)
async def bad_request_exception_handler(request, exc: BadRequestException):
    """
    Custom exception handler for BadRequestException.
    Returns a JSON response with the error message and status code.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "ERROR",
            "message": exc.message,
            "detail": exc.detail,
        },
    )


@router.get("/")
async def read_root():
    return {"Hello": "World"}


def _parse_database_fields(
    rows: list[dict],
) -> list[ProgramPrediction]:
    return [
        ProgramPrediction(
            signal=row.signal,
            program_code=row.program_code,
            weekday=row.weekday,
            available_time=row.total_available_time,
            predicted_audience=row.avg_predicted_audience,
        )
        for row in rows
    ]


@router.get("/program")
async def get_program_predictions(
    request: Annotated[ProgramPredictionCodeRequest, Depends()],
    db: Annotated[SessionLocal, Depends(get_db_session)],
) -> ProgramPredictionResponse:
    """
    Retrieve program predictions by program code and optional weekday.
    """
    from src.database.postgres import get_data_by_program_code

    # Ideally, this would be on a service-layer, not in the HTTP handler.
    # For simplicity, I'm doing it like this.
    predictions_row = get_data_by_program_code(
        request.program_code, request.exhibition_date, db
    )

    response = ProgramPredictionResponse(
        message="Program predictions retrieved successfully.",
        status="SUCCESS",
        body=_parse_database_fields(predictions_row),
    )
    return response


@router.get("/period")
async def get_program_predictions_period(
    request: Annotated[ProgramPredictionPeriodRequest, Depends()],
    db: Annotated[SessionLocal, Depends(get_db_session)],
) -> ProgramPredictionResponse:
    """
    Retrieve program predictions for a specific period by program code.
    """
    from src.database.postgres import get_data_by_period

    predictions_row = get_data_by_period(
        request.program_code, request.start_date, request.end_date, db
    )

    response = ProgramPredictionResponse(
        message="Program predictions for period retrieved successfully.",
        status="SUCCESS",
        body=_parse_database_fields(predictions_row),
    )
    return response


app.include_router(router, tags=["analytics"])
