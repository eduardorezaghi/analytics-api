from dataclasses import dataclass


@dataclass(frozen=True)
class S3ReadCommand:
    bucket: str
    key: str
