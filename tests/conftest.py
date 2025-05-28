import pytest

from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_log_handler():
    """Fixture to mock the logger."""
    with patch('src.commands.s3.handler.logging.getLogger') as mock:
        mock.return_value = MagicMock()
        yield mock

@pytest.fixture
def mock_db_session():
    """Fixture to mock the database session."""
    with patch('src.database.postgres.get_db_session') as mock:
        mock.return_value.__enter__.return_value = MagicMock()
        yield mock