import pytest

from fastapi.testclient import TestClient

from pytest_mock import mocker

from src.api.main import app


@pytest.fixture
def client():
    return TestClient(app)

def test_read_root(client):
    response = client.get("/analytics/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

class DummyRow:
    def __init__(self, signal, program_code, weekday, total_available_time, avg_predicted_audience):
        self.signal = signal
        self.program_code = program_code
        self.weekday = weekday
        self.total_available_time = total_available_time
        self.avg_predicted_audience = avg_predicted_audience

def test_get_program_predictions(mocker, client):
    # Arrange
    rows = [
        DummyRow("sig1", "CASA", "Monday", 120, 1000.0),
        DummyRow("sig2", "CASA", "Tuesday", 150, 1500.0),
    ]
    mocker.patch(
        "src.api.main.get_data_by_program_code",
        return_value=rows
    )
    expected_data = [
        {
            "signal": "sig1",
            "program_code": "CASA",
            "weekday": "Monday",
            "available_time": 120,
            "predicted_audience": 1000.0,
        },
        {
            "signal": "sig2",
            "program_code": "CASA",
            "weekday": "Tuesday",
            "available_time": 150,
            "predicted_audience": 1500.0,
        },
    ]
    
    # Act
    response = client.get("/analytics/program", params={"program_code": "CASA"})
    response_data = response.json()

    # Assert
    assert response.status_code == 200
    assert response_data['message'] == 'Program predictions retrieved successfully.'
    assert response_data['status'] == 'SUCCESS'
    assert response_data['body'] == expected_data


def test_get_program_predictions_by_period(mocker, client):
    # Arrange
    rows = [
        DummyRow("sig1", "CASA", "Monday", 120, 1000.0),
        DummyRow("sig2", "CASA", "Tuesday", 150, 1500.0),
    ]
    mocker.patch(
        "src.api.main.get_data_by_period",
        return_value=rows
    )
    expected_data = [
        {
            "signal": "sig1",
            "program_code": "CASA",
            "weekday": "Monday",
            "available_time": 120,
            "predicted_audience": 1000.0,
        },
        {
            "signal": "sig2",
            "program_code": "CASA",
            "weekday": "Tuesday",
            "available_time": 150,
            "predicted_audience": 1500.0,
        },
    ]

    # Act
    response = client.get("/analytics/period", params={"program_code": "CASA", "start_date": "2023-01-01", "end_date": "2023-01-31"})
    response_data = response.json()

    # Assert
    assert response.status_code == 200
    assert response_data['message'] == 'Program predictions for period retrieved successfully.'
    assert response_data['status'] == 'SUCCESS'
    assert response_data['body'] == expected_data