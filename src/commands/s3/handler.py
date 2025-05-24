import logging

from .command import S3ReadCommand
from boto3 import client
from botocore.exceptions import BotoCoreError, ClientError

class S3ReadHandler:
    def __init__(self,
                 logger: logging.Logger = None,
                 boto3_client=None,
                 ):

        self.logger = logger
        self.boto3_client = boto3_client or self._create_boto3_client()
        self._setup_logging()

    def _create_boto3_client(self):
        import boto3
        return boto3.client('s3')

    def _setup_logging(self):
        if self.logger is None:
            self.logger = logging.getLogger(__name__)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def execute(self, command: S3ReadCommand):
        # Simulate reading from S3
        self.logger.info(f"Executing command: {command}")

        s3_client = self.boto3_client
        try:
            self.logger.info(f"Reading from S3 bucket: {command.bucket}, key: {command.key}")
            response = self._read_from_s3(s3_client, command)
            self.logger.info("Successfully read data from S3")
            return response
        except (BotoCoreError, ClientError) as e:
            self.logger.error(f"Error reading from S3: {e}")


    def _read_from_s3(self, s3_client, command: S3ReadCommand):
        """
        Reads data from an S3 bucket and key specified in the command.
        :param s3_client: Boto3 S3 client
        :param command: S3ReadCommand containing bucket and key
        :return: The content of the S3 object as a string
        """
        response = s3_client.get_object(
            Bucket=command.bucket,
            Key=command.key
        )

        return response['Body'].read().decode('utf-8')