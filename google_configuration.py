import json

from types import SimpleNamespace
from logger.logger_interface import LoggerInterface


class GoogleConfiguration:
    __project_id: str
    __google_credentials_file_path: str

    def __init__(self, config: dict, logger: LoggerInterface) -> None:
        if isinstance(logger, LoggerInterface) is False:
            raise TypeError('Logger instance is not valid!')

        google_credentials_file_path = config.get('credentials_file_path')

        logger.info(f'Opening file... {google_credentials_file_path}')

        with open(google_credentials_file_path, encoding="utf-8") as f:
            data = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

        self.__project_id = data.projectid
        self.__google_credentials_file_path = google_credentials_file_path

    def project_id(self) -> str:
        return self.__project_id

    def google_credentials_file_path(self) -> str:
        return self.__google_credentials_file_path
