from abc import abstractmethod


class LoggerInterface:
    @abstractmethod
    def critical(self, message: str) -> str:
        """Logs critical message into specific output channel."""

    @abstractmethod
    def error(self, message: str) -> str:
        """Logs error message into specific output channel."""

    @abstractmethod
    def warning(self, message: str) -> str:
        """Logs warning message into specific output channel."""

    @abstractmethod
    def info(self, message: str) -> str:
        """Logs info message into specific output channel."""

    @abstractmethod
    def debug(self, message: str) -> str:
        """Logs debug message into specific output channel."""
