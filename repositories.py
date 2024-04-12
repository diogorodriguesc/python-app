from database_client import DatabaseClient


class UsersRepository:
    def __init__(self, database_client: DatabaseClient):
        self.__database_client = database_client

    def create_user(self, username, pwd, role) -> bool:
        try:
            self.__database_client.execute(
                f"""
                INSERT INTO users (\"username\", \"pwd\", \"role\") VALUES ('{username}', '{pwd}', '{role}');
                """
            )
        except Exception:
            # do not let Database exception go out of application
            raise Exception('Unexpected error')

        return True


    def checkIfExists(self, username, pwd) -> list:
        try:
            return self.__database_client.fetchone(
                f"""
                SELECT *
                FROM users where
                username = '{username}'
                AND
                pwd = '{pwd}';
                """
            )

        except Exception:
            raise Exception('Unexpected error')
