from datetime import datetime

class Logger:
    fingers_cross_queue: list

    def __init__(self) -> None:
        self.fingers_cross_queue = list()

    def error(self, message) -> None:
        self.__release_message(self.__format_message(message, 'error'), 'error')

    def warning(self, message) -> None:
        self.__release_message(self.__format_message(message, 'warning'), 'warning')

    def info(self, message) -> None:
        self.__release_message(self.__format_message(message, 'info'), 'info')

    def __format_message(self, message, type) -> str:
        return f"[{self.__datetime()}][{type.upper()}] {message}"
    
    def __release_message(self, message, type):
        if type == 'info':
            self.fingers_cross_queue.append(message)
        else:
            for log in self.fingers_cross_queue:
                print(log)
            print(message)

            self.fingers_cross_queue = list()

    def __datetime(self) -> str:
        now = datetime.now()
        return now.strftime('%Y-%m-%d %H:%M:%S')