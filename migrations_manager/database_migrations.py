import os
import importlib.util

import psycopg2
from logger.logger_interface import LoggerInterface


class DatabaseMigrations:
    __DIRECTORY_FOR_MIGRATIONS="migrations_manager/migrations"

    __migrations_manager_repository = None
    __migrations_executor = None

    __logger: LoggerInterface

    def __init__(self, connection, logger: LoggerInterface) -> None:
        self.__migrations_manager_repository = MigrationsManagerRepository(connection)
        self.__migrations_executor = MigrationExecutor(connection)
        self.__logger = logger

    def migrate(self):
        self.__migrations_manager_repository.create_migrations_table_if_not_exists()

        for filename in sorted(os.listdir(self.__DIRECTORY_FOR_MIGRATIONS)):
            if filename.endswith(".py"):
                self.__migrate_file(filename)

        self.__logger.info(f"All migrations_manager applied")

    def __migrate_file(self, filename: str) -> None:
        if self.__migrations_manager_repository.check_if_migrated(filename) is False:
            self.__logger.info(f"{filename} is not migrated, migration will take place")
            self.__migrations_manager_repository.insert_migration(filename)
            obj = self.__load_module(filename, f"{self.__DIRECTORY_FOR_MIGRATIONS}/{filename}")
            obj.up()

    def __load_module(self, filename: str, location: str) -> object:
        spec = importlib.util.spec_from_file_location(filename, location)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return getattr(module, filename[:-3])()


class DatabaseClient:
    _connection = None

    def __init__(self, connection) -> None:
        self._connection = connection


class MigrationExecutor(DatabaseClient):
    def execute(self, query: str) -> None:
        cursor = self._connection.cursor()
        cursor.execute(query)
        self._connection.commit()


class MigrationsManagerRepository(DatabaseClient):
    def check_if_migrated(self, filename: str) -> bool:
        cursor = self._connection.cursor()
        cursor.execute(
            f"""
            SELECT * FROM migrations WHERE file = '{filename}';
            """
        )
        results = cursor.rowcount

        if results == 0:
            return False

        return True

    def insert_migration(self, filename: str) -> None:
        self._connection.cursor().execute(
            f"""
            INSERT INTO migrations (file) VALUES ('{filename}');
            """
        )

        self._connection.commit()

    def create_migrations_table_if_not_exists(self) -> None:
        self._connection.cursor().execute(
            """
            CREATE TABLE IF NOT EXISTS migrations(file VARCHAR (200) UNIQUE NOT NULL);
            """
        )

        self._connection.commit()
