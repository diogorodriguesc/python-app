class Version20240102:
    def up(self) -> str:
        return f'CREATE TABLE "users" ("id" SERIAL,"username" varchar,"pwd" varchar,"role" varchar, PRIMARY KEY ("id"));'

    def down(self) -> None:
        raise Exception("Not revertable")
