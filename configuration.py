import json
import os

from types import SimpleNamespace
from logger.logger_interface import LoggerInterface


class Configuration:
    __project_id: str
    __google_credentials_file_path: str

    def __init__(self, config: dict, logger: LoggerInterface) -> None:
        if isinstance(logger, LoggerInterface) is False:
            raise TypeError('Logger instance is not valid!')
        
        google_credentials_file_path = os.getenv(config.get('credentials_file_path'))
        if google_credentials_file_path is None:
            raise Exception(f'Environment variable missing!')

        logger.info(f'Opening file... {google_credentials_file_path}');
        f = open(google_credentials_file_path)

        data = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
        self.__project_id = data.projectid
        self.__google_credentials_file_path = google_credentials_file_path

        f.close()

    def project_id(self) -> str:
        return self.__project_id

    def google_credentials_file_path(self) -> str:
        return self.__google_credentials_file_path
