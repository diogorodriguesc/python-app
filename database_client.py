import psycopg2


class DatabaseClient:
    __config: dict

    def __init__(self, config):
        self.__config = config

    def __connect(self):
        try:
            return psycopg2.connect(
                host=self.__config.get('host'),
                port=self.__config.get('port'),
                database=self.__config.get('database'),
                user=self.__config.get('user'),
                password=self.__config.get('password')
            )
        except Exception:
            raise Exception("Could not connect to database")

    def execute(self, query):
        connection = self.__connect()
        connection.cursor().execute(query)
        connection.commit()
        connection.close()

    def fetchone(self, query):
        connection = self.__connect()
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchone()
        cursor.close()

        return results
