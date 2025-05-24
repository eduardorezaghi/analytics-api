import pytest

from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_log_handler():
    """Fixture to mock the logger."""
    with patch('src.commands.s3.handler.logging.getLogger') as mock:
        mock.return_value = MagicMock()
        yield mock
