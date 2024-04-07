def run(environment: str) -> None:
    from container import Container
    try:
        container = Container(environment)

        container.get_database_migrations().migrate()
    except Exception as exception:
        print(exception)


if __name__ == "__main__":
    import sys

    if sys.argv[1] == "run_migrations":
        print("Running migrations")

        import os
        run(os.getenv("SITEMAPS_INDEXING_ENVIRONMENT"))
