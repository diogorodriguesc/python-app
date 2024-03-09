import os
import yaml

from logger.text_formatter import TextFormatter
from logger.logger import Logger
from logger.logger_interface import LoggerInterface
from configuration import Configuration

CONFIG_FILES = {'dev': '../config/dev/parameters.yaml', 'prod': '../config/prod/parameters.yaml'}
ENVIRONMENTS = ['dev', 'test', 'prod']

class Container:
    logger: any
    environment: str
    parameters: dict
    configuration: any

    def __init__(self, environment: str) -> None:
        if environment not in ENVIRONMENTS:
            raise Exception(f'Environment {environment} is not valid! It must be one of: {ENVIRONMENTS}')

        self.logger = self.configuration = None
        self.environment = environment
        with open(CONFIG_FILES.get(environment), 'r') as file:
            self.parameters = yaml.safe_load(file)['parameters']

        self.getLogger().info(f'Environment selected: {self.environment}')

    def getLogger(self) -> LoggerInterface:
        if self.logger is None:
            self.logger = Logger(self.getParameters().get('logger'), TextFormatter())

        return self.logger
    
    def getGoogleConfiguration(self) -> Configuration:
        if self.configuration is None:
            self.configuration = Configuration(self.getParameters().get('google'), self.getLogger())

        return self.configuration
    
    def getParameters(self) -> dict:
        return self.parameters
