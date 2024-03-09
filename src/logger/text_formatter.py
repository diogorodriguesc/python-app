from datetime import datetime

class TextFormatter:
    def __init__(self) -> None:
        pass

    def format(self, message: str, log_level: str) -> str:
        return f"[{self.__datetime()}][{log_level.upper()}] {message}"
    
    def __datetime(self) -> str:
        return (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')