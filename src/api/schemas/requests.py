import datetime

from pydantic import BaseModel, Field, model_validator

from src.api.exceptions import BadRequestException


class ProgramPredictionCodeRequest(BaseModel):
    program_code: str = Field(
        ..., description="Program code to filter the data", example="program_123"
    )
    exhibition_date: datetime.datetime | None = Field(
        None,
        description="Optional exhibition date to filter the data",
        example="2023-01-01",
    )

class ProgramPredictionPeriodRequest(BaseModel):
    """
    Schema for requesting period data.
    """

    program_code: str = Field(
        ..., description="Program code to filter the data", example="program_123"
    )
    start_date: datetime.datetime = Field(
        ..., description="Start date of the period", example="2023-01-01T00:00:00"
    )
    end_date: datetime.datetime = Field(
        ..., description="End date of the period", example="2023-01-31T23:59:59"
    )

    @model_validator(mode="before")
    def validate_dates(cls, values):
        """
        Validate that start_date is before end_date.
        """
        start_date = values.get("start_date")
        end_date = values.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise BadRequestException(
                "INCONSISTENT_DATES", "Start date must be before end date."
            )

        return values
