import os
import sys

GOOGLE_CREDENTIALS_ENV_VAR = 'GOOGLE_CREDENTIALS'

from container import Container
from configuration import Configuration

def run():
    try:
        container = Container(sys.argv[1])

        google_credentials = os.getenv(GOOGLE_CREDENTIALS_ENV_VAR)
        if google_credentials is None:
            raise Exception(f'{GOOGLE_CREDENTIALS_ENV_VAR} environment variable missing!')
    
        configuration = Configuration(google_credentials, container.getLogger())
    except Exception as exception:
        #container.getLogger().critical(exception)
        print(exception)

if __name__ == '__main__':
    run()