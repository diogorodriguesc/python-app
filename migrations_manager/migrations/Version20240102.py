class Version20240102:
    @staticmethod
    def up() -> str:
        return 'CREATE TABLE "users" ("id" SERIAL,"username" varchar UNIQUE,"pwd" varchar,"role" varchar, PRIMARY KEY ("id"));'

    @staticmethod
    def down() -> None:
        raise Exception("Not revertable")
