from abc import ABC, abstractmethod
from typing import Any, Optional
from .s3 import S3ReadCommand, S3ReadHandler


class Command(ABC):
    """
    Abstract base class for commands.
    All commands should inherit from this class and implement the `execute` method.
    """

    @abstractmethod
    def handle(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        """
        Execute the command with the given arguments.
        This method should be implemented by all subclasses.
        """
        pass

    def __str__(self):
        """
        Return a string representation of the command.
        This method can be overridden by subclasses to provide a custom string representation.
        """
        return f"{self.__class__.__name__}()"


__all__ = [
    "Command",
    "S3ReadCommand",
    "S3ReadHandler",
]
