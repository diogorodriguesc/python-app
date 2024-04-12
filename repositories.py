class UsersRepository:
    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def create_user(self, username, pwd, role) -> bool:
        try:
            self.__connection.cursor().execute(
                f"""
                INSERT INTO users (\"username\", \"pwd\", \"role\") VALUES ('{username}', '{pwd}', '{role}');
                """
                )
            self.__connection.commit()
        except Exception:
            # do not let Database exception go out of application
            raise Exception('Unexpected error')

        return True


    def checkIfExists(self, username, pwd) -> list:
        try:
            cursor = self.__connection.cursor()
            cursor.execute(
                f"""
                SELECT *
                FROM users where
                username = '{username}'
                AND
                pwd = '{pwd}';
                """
            )

            return cursor.fetchone()
        except Exception:
            raise Exception('Unexpected error')
