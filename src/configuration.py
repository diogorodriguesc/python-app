import os
import json

from types import SimpleNamespace
from logger.logger_interface import LoggerInterface

class Configuration:
    __projectId: str
    __googleCredentialsFilePath: str

    def __init__(self, config: dict, logger: LoggerInterface) -> None:
        if isinstance(logger, LoggerInterface) is False:
            raise TypeError('Logger instance is not valid!')
        
        googleCredentialsFilePath = os.getenv(config.get('credentials_file_path'))
        if googleCredentialsFilePath is None:
            raise Exception(f'Environment variable missing!')

        logger.info(f'Opening file... {googleCredentialsFilePath}');
        f = open(googleCredentialsFilePath)

        data = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
        self.__projectId = data.projectid
        self.__googleCredentialsFilePath = googleCredentialsFilePath

        f.close()

    def projectId(self) -> str:
        return self.__projectId

    def googleCredentialsFilePath(self) -> str:
        return self.__googleCredentialsFilePath
