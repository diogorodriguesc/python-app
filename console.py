import os
import sys

from container import Container


def run(environment: str) -> None:
    try:
        container = Container(environment)

        container.get_database_migrations().migrate()
    except Exception as exception:
        print(exception)


if __name__ == "__main__":
    if sys.argv[1] == "run_migrations":
        run(os.getenv("SITEMAPS_INDEXING_ENVIRONMENT"))
