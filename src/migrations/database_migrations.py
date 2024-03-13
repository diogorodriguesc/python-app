import psycopg2

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
        self.__logger.info("Migrating...")

        self.__create_migrations_table_if_not_exists()

    def __create_migrations_table_if_not_exists(self) -> None:
        cursor = self.__conn.cursor()
        cursor.execute("""SELECT tablename FROM pg_tables WHERE tablename = 'migrations';""")
        rows = cursor.fetchall()

        if not rows:
            self.__conn.cursor().execute("""CREATE TABLE IF NOT EXISTS migrations(
                file VARCHAR (200) UNIQUE NOT NULL);
                """)

            self.__conn.commit()

            self.__logger.info("create migrations table")