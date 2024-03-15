import yaml
import psycopg2

from configuration import Configuration
from logger.formatters.text_formatter import TextFormatter
from logger.logger import Logger
from logger.logger_interface import LoggerInterface
from migrations.database_migrations import DatabaseMigrations

CONFIG_FILES = {'dev': '../config/dev/parameters.yaml', 'prod': '../config/prod/parameters.yaml'}
ENVIRONMENTS = ['dev', 'test', 'prod']


class Container:
    __logger: any = None
    __environment: str = None
    __parameters: dict = None
    __configuration: any = None
    __database_migrations: any = None
    __database_connection: any = None

    def __init__(self, environment: str) -> None:
        if environment not in ENVIRONMENTS:
            raise Exception(f'Environment {environment} is not valid! It must be one of: {ENVIRONMENTS}')

        self.__environment = environment
        with open(CONFIG_FILES.get(environment), 'r') as file:
            self.__parameters = yaml.safe_load(file)['parameters']

        self.get_logger().info(f'Environment selected: {self.__environment}')

    def get_logger(self) -> LoggerInterface:
        if self.__logger is None:
            self.__logger = Logger(self.get_parameters().get('logger'), TextFormatter())

        return self.__logger

    def get_google_configuration(self) -> Configuration:
        if self.__configuration is None:
            self.__configuration = Configuration(self.get_parameters().get('google'), self.get_logger())

        return self.__configuration

    def get_parameters(self) -> dict:
        return self.__parameters

    def get_database_migrations(self) -> DatabaseMigrations:
        if self.__database_migrations is None:
            self.__database_migrations = DatabaseMigrations(
                self.__get_database_connection(),
                logger=self.get_logger()
            )

        return self.__database_migrations

    def __get_database_connection(self):
        if self.__database_connection is None:
            database_configs = self.get_parameters().get('database')

            self.__database_connection = psycopg2.connect(
                host=database_configs.get('host'),
                port=database_configs.get('port'),
                database=database_configs.get('database'),
                user=database_configs.get('user'),
                password=database_configs.get('password')
            )

        return self.__database_connection
