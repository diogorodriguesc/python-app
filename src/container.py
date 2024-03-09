import yaml

from logger.logger import Logger
from logger.logger_interface import LoggerInterface

CONFIG_FILES = {'dev': '../config/dev/parameters.yaml', 'prod': '../config/prod/parameters.yaml'}
ENVIRONMENTS = ['dev', 'test', 'prod']

class Container:
    logger: any
    environment: str
    parameters: dict

    def __init__(self, environment: str) -> None:
        if environment not in ENVIRONMENTS:
            raise Exception(f'Environment {environment} is not valid! It must be one of: {ENVIRONMENTS}')

        self.logger = None
        self.environment = environment;
        with open(CONFIG_FILES.get(environment), 'r') as file:
            self.parameters = yaml.safe_load(file)['parameters']

        self.getLogger().info(f'Environment selected: {self.environment}')

    def getLogger(self) -> LoggerInterface:
        if self.logger is None:
            self.logger = Logger(self.getParameters().get('logger'))

        return self.logger

    def getParameters(self) -> dict:
        return self.parameters
