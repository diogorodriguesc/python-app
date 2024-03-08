class Configuration:
    projectId: str
    googleCredentialsFilePath: str

    def __init__(self, projectId: str, googleCredentialsFilePath: str) -> None:
        self.__projectId = projectId
        self.__googleCredentialsFilePath = googleCredentialsFilePath

    def projectId(self) -> str:
        return self.__projectId

    def googleCredentialsFilePath(self) -> str:
        return self.__googleCredentialsFilePath