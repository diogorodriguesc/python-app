from abc import abstractmethod, ABCMeta


class FormatterInterface(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def format(self, message: str, log_level: str) -> str:
        """format the message."""
