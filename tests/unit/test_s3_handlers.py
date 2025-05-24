import pytest
from unittest.mock import patch, MagicMock
import logging


from src.commands import S3ReadHandler, S3ReadCommand


@pytest.fixture
def mock_s3_client():
    """Fixture to mock the S3 client."""
    with patch('src.commands.s3.handler.client') as mock:
        mock.return_value = MagicMock()
        mock.get_object.return_value = {
            'Body': MagicMock(read=lambda: b'This is a test file content')
        }
        yield mock
    ...


def test_correctly_reads_from_s3(mock_s3_client, mock_log_handler):
    """Test the S3ReadHandler's read_from_s3 method."""
    # Arrange
    handler = S3ReadHandler(
        boto3_client=mock_s3_client,
        logger=mock_log_handler,
    )
    
    # Act
    command = S3ReadCommand(bucket='test-bucket', key='test-key')
    result = handler.execute(command)

    # Assert
    assert result == 'This is a test file content'
    assert mock_s3_client.get_object.called
    assert mock_log_handler.info.called

    mock_s3_client.get_object.assert_called_once_with(Bucket='test-bucket', Key='test-key')
    
    # Assert log calls.z
    assert mock_log_handler.info.call_count == 3
    assert mock_log_handler.info.call_args_list[0][0][0] == "Executing command: S3ReadCommand(bucket='test-bucket', key='test-key')"
    assert mock_log_handler.info.call_args_list[1][0][0] == "Reading from S3 bucket: test-bucket, key: test-key"
    assert mock_log_handler.info.call_args_list[2][0][0] == "Successfully read data from S3"

