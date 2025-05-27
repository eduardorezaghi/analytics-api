from pydantic import BaseModel, Field


class ResponseSchema(BaseModel):
    """
    Base schema for API responses.
    """
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Status of the response", example="success")
    body: dict | None = Field(
        None, description="Optional body of the response containing data"
    )

    class Config:
        schema_extra = {
            "example": {
                "message": "Request processed successfully.",
                "status": "success"
            }
        }

class ProgramPrediction(BaseModel):
    signal: str = Field(..., description="Signal identifier")
    program_code: str = Field(..., description="Program code")
    weekday: str = Field(..., description="Day of the week")
    available_time: int = Field(..., description="Time when the program is available")
    predicted_audience: float = Field(..., description="Predicted audience count", example=1000)


class ProgramPredictionResponse(ResponseSchema):
    """
    Schema for program prediction responses.
    """
    body: list[ProgramPrediction] = Field(
        ...,
        description="List of program predictions",
        example=[
            {
                "signal": "signal_1",
                "program_code": "program_1",
                "weekday": "Monday",
                "available_time": "10:00",
                "predicted_audience": 1000
            }
        ]
    )