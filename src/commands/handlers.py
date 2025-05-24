from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from . import Command


class Handler(ABC):
    """
    Abstract base class for command handlers.
    """

    @abstractmethod
    def execute(self, command: Command) -> Any:
        """
        Execute the command.
        :param command: The command to execute.
        :return: The result of the command execution.
        """
        pass