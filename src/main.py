import sys

from container import Container

def run():
    try:
        container = Container(sys.argv[1])
        container.getLogger().info(f'Projectid is: {container.getGoogleConfiguration().projectId()}')
    except Exception as exception:
        #container.getLogger().critical(exception)
        print(exception)

if __name__ == '__main__':
    run()