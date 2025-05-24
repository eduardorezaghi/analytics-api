from src.lambdas.import_csv_lambda import handler
from unittest.mock import patch, MagicMock

from src.commands.handlers import Handler
from src.commands.bus import CommandBus
from src.commands.s3 import S3ReadCommand

import pytest
from pytest_mock import mocker

@pytest.fixture
def fake_handler(mocker):
    mock_handler = mocker.Mock(spec=Handler)
    mock_handler.execute.return_value = "Mocked result"

    return mock_handler


def test_lambda_handler(mocker, fake_handler):
    # Mock the command bus and its dispatch method
    command_bus = CommandBus()
    command_bus.register(S3ReadCommand, fake_handler)
    mock_command_bus = mocker.patch('src.lambdas.import_csv_lambda.get_command_bus', return_value=command_bus)

    # Create a mock event and context
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": 'test-bucket'},
                    "object": {"key": 'test-key'}
                }
            }
        ]
    }
    context = MagicMock()

    # Call the handler function
    result = handler(event, context)

    assert result == "Mocked result"
    mock_command_bus.assert_called_once()
    cmd = S3ReadCommand(bucket='test-bucket', key='test-key')
    fake_handler.execute.assert_called_once_with(cmd)