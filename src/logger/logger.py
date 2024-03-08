from datetime import datetime

class Logger:
    fingers_cross: bool
    fingers_cross_queue: list
    
    def __init__(self, config: dict) -> None:
        self.fingers_cross = config.get('fingers_cross', False)
        self.fingers_cross_queue = list()

    def critical(self, message) -> None:
        self.__release_message(self.__format_message(message, 'critical'), 'critical')

    def error(self, message) -> None:
        self.__release_message(self.__format_message(message, 'error'), 'error')

    def warning(self, message) -> None:
        self.__release_message(self.__format_message(message, 'warning'), 'warning')

    def info(self, message) -> None:
        self.__release_message(self.__format_message(message, 'info'), 'info')

    def debug(self, message) -> None:
        self.__release_message(self.__format_message(message, 'debug'), 'debug')

    def __format_message(self, message, type) -> str:
        return f"[{self.__datetime()}][{type.upper()}] {message}"
    
    def __release_message(self, message, type):
        if self.fingers_cross is True:
            if type == 'debug':
                self.fingers_cross_queue.append(message)
            else:
                for log in self.fingers_cross_queue:
                    print(log)
                print(message)

                self.fingers_cross_queue = list()
        else:
            print(message)

    def __datetime(self) -> str:
        now = datetime.now()
        return now.strftime('%Y-%m-%d %H:%M:%S')