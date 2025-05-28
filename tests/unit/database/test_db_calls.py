from dataclasses import dataclass
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

@dataclass
class ProgramPredictionRow:
    signal: str
    program_code: str
    weekday: str
    total_available_time: int
    avg_predicted_audience: int

@pytest.mark.asyncio
@pytest.mark.skip("Skipping test_get_program_predictions due to database dependency")
async def test_get_data_by_program_code(mocker,):
    """
    Tests the get_data_by_program_code function with a mocked database session.
    """
    mock_return_data = [
        ("signal1", "CASA", "Monday", 120, 1500.0),
        ("signal2", "CASA", "Tuesday", 180, 2500.0),
    ]

    # 2. Use patch to mock the 'get_async_session' function
    with mocker.patch("src.database.postgres.get_async_session", new_callable=mocker.AsyncMock) as mock_get_session:
        mock_session = mocker.AsyncMock()
        mock_result = mocker.AsyncMock()
        mock_result.all.return_value = mock_return_data

        mock_session.execute = mocker.AsyncMock(return_value=mock_result)
        mock_get_session.return_value.__aenter__.return_value = mock_session

        program_code = "CASA"
        result = await get_data_by_program_code(program_code=program_code)

        assert result == mock_return_data

        mock_session.execute.assert_called_once()

@pytest.mark.asyncio
@pytest.mark.skip("Skipping test_get_data_by_program_code due to database dependency")
async def test_get_data_by_period(
    mocker,
):
    from src.database.postgres import get_data_by_period
    from src.models import ProgramPrediction
    
    # Arrange
    program_prediction_row = ProgramPredictionRow(
        signal="test_signal",
        program_code="test_program_code",
        weekday="Monday",
        total_available_time=120,
        avg_predicted_audience=300,
    )
    mocker.patch(
        "src.database.postgres.get_async_session",
        return_value=mocker.AsyncMock(),
    )
    mocker.get_async_session().execute.return_value.all.return_value = [program_prediction_row]


    # Act
    result = await get_data_by_period("test_program_code", "2025-05-01", "2025-07-31")
    
    assert result == [program_prediction_row]
    mocker.get_async_session().execute.assert_called_once()