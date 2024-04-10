from flask import Flask
from auth_middleware import authenticator
from container import Container
import os
from models import User

app = Flask(__name__)
container = Container(os.getenv("SITEMAPS_INDEXING_ENVIRONMENT"))
app.config['SECRET_KEY'] = container.get_parameters().get('authentication')['secret_key']


@app.route("/")
def home():
    return "Hello World!"


@app.get("/urls")
@authenticator("ROLE_ADMIN")
def urls(current_user: User):
    if type(current_user) is User:
        return f"Hello World {current_user.get_name()}"


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as exception:
        print(exception)
