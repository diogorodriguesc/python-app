class LoggerInterface:
    def critical(self, message: str) -> str:
        """Logs critical message into specific output channel."""
        pass

    def error(self, message: str) -> str:
        """Logs error message into specific output channel."""
        pass

    def warning(self, message: str) -> str:
        """Logs warning message into specific output channel."""
        pass

    def info(self, message: str) -> str:
        """Logs info message into specific output channel."""
        pass

    def debug(self, message: str) -> str:
        """Logs debug message into specific output channel."""
        pass