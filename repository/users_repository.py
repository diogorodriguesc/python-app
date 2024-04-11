class UsersRepository:

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def create_user(self, username, pwd, role):
        self.__connection.cursor().execute(f"INSERT INTO users (\"username\", \"pwd\", \"role\") VALUES ('{username}', '{pwd}', '{role}');")
        self.__connection.commit()

    def checkIfExists(self, username, pwd) -> list:
        cursor = self.__connection.cursor()
        cursor.execute(
            f"""
            select *
            from users where
            username = '{username}'
            AND
            pwd = '{pwd}';
            """
        )

        return cursor.fetchone()
