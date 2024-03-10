import sys

from container import Container


def run():
    try:
        container = Container(sys.argv[1])
        container.get_logger().info(f'Project id is: {container.get_google_configuration().project_id()}')
    except Exception as exception:
        print(exception)


if __name__ == '__main__':
    run()