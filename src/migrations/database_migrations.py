import psycopg2
import os
import importlib.util

from logger.logger_interface import LoggerInterface


class DatabaseMigrations:
    __connection = None
    __logger: LoggerInterface

    def __init__(self, host: str, port: int, database: str, user: str, password: str, logger: LoggerInterface) -> None:
        self.__conn = psycopg2.connect(
            database=database,
            user=user,
            host=host,
            password=password,
            port=port
        )
        self.__logger = logger

    def migrate(self):
        self.__create_migrations_table_if_not_exists()

        for filename in sorted(os.listdir("../migrations")):
            if filename.endswith(".py"):
                self.__migrate_file(filename)

    def __migrate_file(self, filename: str) -> None:
        self.__logger.info(f"Migrating {filename}...")

        if self.__check_if_migrated(filename):
            self.__logger.info(f"{filename} is migrated")
        else:
            self.__logger.info(f"{filename} is not migrated, migration will take place")
            self.__insert_migration(filename)
            obj = self.__load_module(filename, f"../migrations/{filename}")
            obj.up()

    def __load_module(self, filename: str, location) -> object:
        spec = importlib.util.spec_from_file_location(filename, location)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return getattr(module, filename[:-3])()

    def __check_if_migrated(self, filename: str) -> bool:
        cursor = self.__conn.cursor()
        cursor.execute(f"""SELECT * FROM migrations WHERE file = '{filename}'""")
        results = cursor.rowcount

        if results == 0:
            return False

        return True

    def __insert_migration(self, filename: str) -> None:
        self.__conn.cursor().execute(f"""
        INSERT INTO migrations (file) VALUES ('{filename}')
                        """)

        self.__conn.commit()

    def __create_migrations_table_if_not_exists(self) -> None:
        self.__conn.cursor().execute("""CREATE TABLE IF NOT EXISTS migrations(
            file VARCHAR (200) UNIQUE NOT NULL);
            """)

        self.__conn.commit()