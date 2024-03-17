from datetime import datetime

from ..formatter_interface import FormatterInterface


def get_datetime_string() -> str:
    return (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')


class TextFormatter(FormatterInterface):
    def __init__(self) -> None:
        pass

    def format(self, message: str, log_level: str) -> str:
        return f"[{get_datetime_string()}][{log_level.upper()}] {message}"
