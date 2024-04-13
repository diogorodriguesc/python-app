from __future__ import annotations


class Response:
    __data: dict | None
    __message: str | None
    __error: str | None

    def __init__(self, data=None, message=None, error=None):
        self.__data = data
        self.__message = message
        self.__error = error

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
        self.__name = f'user_{self.__user_id}'
        self.__role = role

    def get_name(self) -> str:
        return self.__name

    def get_role(self) -> str:
        return self.__role
