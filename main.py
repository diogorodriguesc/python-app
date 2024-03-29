def run() -> None:
    try:
        container = Container(sys.argv[1])
        container.get_logger().info(f'Project id is: {container.get_google_configuration().project_id()}')

        container.get_database_migrations().migrate()
    except Exception as exception:
        print(exception)


if __name__ == '__main__':
    import sys

    from container import Container
    run()
