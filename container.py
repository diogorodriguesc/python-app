import os
import psycopg2
import yaml

from google_configuration import GoogleConfiguration
from migrations_manager.database_migrations import DatabaseMigrations
from logger import (
    TextFormatter,
    Logger,
    LoggerInterface
)
from repositories import UsersRepository

from database_client import DatabaseClient

CONFIG_FILES = {'dev': 'config/dev/parameters.yaml', 'prod': 'config/prod/parameters.yaml'}
ENVIRONMENTS = ['dev', 'test', 'prod']


def extract_configurations(environment: str) -> dict:
    with open(CONFIG_FILES.get(environment), 'r', encoding="UTF-8") as file:
        return replace_env_variables(yaml.safe_load(file)['parameters'])


def replace_env_variables(data):
    data1 = None
    if isinstance(data, dict):
        data1 = data.items()
    if isinstance(data, list):
        data1 = enumerate(data)

    if data1 is not None:
        for key, value in data1:
            if isinstance(value, (dict, list)):
                replace_env_variables(value)
            elif isinstance(value, str) and '%' in value:
                env_var_name = value.strip('%')
                env_var_value = os.getenv(env_var_name)
                if env_var_value is not None:
                    data[key] = env_var_value

    return data


class Container:
    __logger: LoggerInterface = None
    __environment: str = None
    __parameters: dict = None
    __google_configuration: GoogleConfiguration = None
    __database_migrations: DatabaseMigrations = None
    __database_connection: any = None
    __users_repository: UsersRepository = None
    __database_configs: any = None
    __database_client: DatabaseClient = None

    def __init__(self, environment: str) -> None:
        if environment not in ENVIRONMENTS:
            raise Exception(f'Environment {environment} is not valid! It must be one of: {ENVIRONMENTS}')

        self.__environment = environment
        self.__parameters = extract_configurations(environment)
        self.get_logger().info(f'Environment selected: {self.__environment}')

    def get_logger(self) -> LoggerInterface:
        if self.__logger is None:
            self.__logger = Logger(self.get_parameters().get('logger'), TextFormatter())

        return self.__logger

    def get_google_configuration(self) -> GoogleConfiguration:
        if self.__google_configuration is None:
            self.__google_configuration = GoogleConfiguration(self.get_parameters().get('google'), self.get_logger())

        return self.__google_configuration

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
            database_configs = self.__get_database_configuration()

            self.__database_connection = psycopg2.connect(
                host=database_configs.get('host'),
                port=database_configs.get('port'),
                database=database_configs.get('database'),
                user=database_configs.get('user'),
                password=database_configs.get('password')
            )

        return self.__database_connection

    def __get_database_configuration(self):
        if self.__database_configs is None:
            self.__database_configs = self.get_parameters().get('database')

        return self.__database_configs

    def __get_database_client(self) -> DatabaseClient:
        if self.__database_client is None:
            self.__database_client = DatabaseClient(self.__get_database_configuration())

        return self.__database_client

    def get_users_repository(self) -> UsersRepository:
        if self.__users_repository is None:
            self.__users_repository = UsersRepository(self.__get_database_client())

        return self.__users_repository
