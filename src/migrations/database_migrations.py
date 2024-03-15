import psycopg2
import os
import importlib.util

from logger.logger_interface import LoggerInterface


class DatabaseConfig:
    __host: str
    __port: int
    __database: str
    __user: str
    __password: str

    def __init__(self, host: str, port: int, database: str, user: str, password: str) -> None:
        self.__host = host
        self.__port = port
        self.__database = database
        self.__user = user
        self.__password = password

    def get_host(self) -> str:
        return self.__host

    def get_port(self) -> int:
        return self.__port

    def get_database(self) -> str:
        return self.__database

    def get_user(self) -> str:
        return self.__user

    def get_password(self) -> str:
        return self.__password


class DatabaseMigrations:
    __migrations_manager_repository = None
    __migrations_executer = None

    __logger: LoggerInterface

    def __init__(self, database_config: DatabaseConfig, logger: LoggerInterface) -> None:
        self.__migrations_manager_repository = MigrationsManagerRepository(database_config)
        self.__migrations_executer = MigrationExecuter(database_config)
        self.__logger = logger

    def migrate(self):
        self.__migrations_manager_repository.create_migrations_table_if_not_exists()

        for filename in sorted(os.listdir("../migrations")):
            if filename.endswith(".py"):
                self.__migrate_file(filename)

    def __migrate_file(self, filename: str) -> None:
        self.__logger.info(f"Migrating {filename}...")

        if self.__migrations_manager_repository.check_if_migrated(filename):
            self.__logger.info(f"{filename} is migrated")
        else:
            self.__logger.info(f"{filename} is not migrated, migration will take place")
            self.__migrations_manager_repository.insert_migration(filename)
            obj = self.__load_module(filename, f"../migrations/{filename}")
            obj.up()

    def __load_module(self, filename: str, location: str) -> object:
        spec = importlib.util.spec_from_file_location(filename, location)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return getattr(module, filename[:-3])()


class DatabaseClient:
    _conn = None

    def __init__(self, database_config: DatabaseConfig) -> None:
        self._conn = psycopg2.connect(
            database=database_config.get_database(),
            user=database_config.get_user(),
            host=database_config.get_host(),
            password=database_config.get_password(),
            port=database_config.get_port()
        )


class MigrationExecuter(DatabaseClient):
    def execute(self, query: str) -> None:
        cursor = self._conn.cursor()
        cursor.execute(query)
        self._conn.commit()


class MigrationsManagerRepository(DatabaseClient):
    def check_if_migrated(self, filename: str) -> bool:
        cursor = self._conn.cursor()
        cursor.execute(f"""SELECT * FROM migrations WHERE file = '{filename}'""")
        results = cursor.rowcount

        if results == 0:
            return False

        return True

    def insert_migration(self, filename: str) -> None:
        self._conn.cursor().execute(f"""
        INSERT INTO migrations (file) VALUES ('{filename}')
                        """)

        self._conn.commit()

    def create_migrations_table_if_not_exists(self) -> None:
        self._conn.cursor().execute("""CREATE TABLE IF NOT EXISTS migrations(
            file VARCHAR (200) UNIQUE NOT NULL);
            """)

        self._conn.commit()
