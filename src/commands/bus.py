
from typing import Type, Dict, List

from . import Command
from .handlers import Handler
from .s3 import S3ReadCommand, S3ReadHandler

class CommandBus:
    def __init__(self):
        self._handlers: Dict[Type[Command], Handler] = {}

    def register(self, command_type: Type[Command], handler: Handler):
        self._handlers[command_type] = handler

    def dispatch(self, cmd):
        handler = self._handlers.get(type(cmd))
        if handler is None:
            raise ValueError(f"No handler registered for command type: {type(cmd)}")

        return handler.execute(cmd)


def get_command_bus() -> CommandBus:
    """
    Returns the command bus instance.
    This function is used to access the command bus from different parts of the application.
        """
    command_bus = CommandBus()
    command_bus.register(S3ReadCommand, S3ReadHandler())
    return command_bus