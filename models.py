class Response:
    __data: dict
    __message: str
    __error: str

    def __init__(self, data: any, message: any, error: any):
        self.__data = data or None
        self.__message = message or None
        self.__error = error or None

    def parse(self) -> dict:
        return {
            "data": self.__data,
            "message": self.__message,
            "error": self.__error
        }


class User:
    __user_id: int
    __name: str
    __role: str

    def __init__(self, user_id: int, role: str):
        self.__user_id = user_id
        self.__name = f'user_{user_id}'
        self.__role = role

    def get_name(self):
        return self.__name

    def get_role(self):
        return self.__role
