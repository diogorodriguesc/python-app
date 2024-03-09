import json

from types import SimpleNamespace

class Configuration:
    projectId: str
    googleCredentialsFilePath: str

    def __init__(self, googleCredentialsFilePath: str) -> None:
        f = open(googleCredentialsFilePath)

        data = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
        self.__projectId = data.projectid
        self.__googleCredentialsFilePath = googleCredentialsFilePath

        f.close()

    def projectId(self) -> str:
        return self.__projectId

    def googleCredentialsFilePath(self) -> str:
        return self.__googleCredentialsFilePath
