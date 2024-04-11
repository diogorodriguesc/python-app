from flask import Flask, request
from auth_middleware import auth_required, authenticate_user, register_user
from container import Container
import os
from models import User

app = Flask(__name__)
container = Container(os.getenv("SITEMAPS_INDEXING_ENVIRONMENT"))
app.config['SECRET_KEY'] = container.get_parameters().get('authentication')['secret_key']


@app.get("/urls")
@auth_required("ROLE_ADMIN", container.get_users_repository())
def urls(current_user: User):
    if type(current_user) is User:
        return {

        }


@app.post("/sign_in")
def sign_in():
    try:
        return authenticate_user(request.json, container.get_users_repository())
    except Exception as e:
        return {
            "message": str(e)
        }, 500


@app.post("/sign_up")
def sign_up():
    try:
        return register_user(request.json, container.get_users_repository())
    except Exception as e:
        return {
            "message": str(e)
        }, 500


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as exception:
        container.get_logger().critical(str(exception))
