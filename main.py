import os
from flask import Flask, request

from auth_middleware import auth_required, authenticate_user, register_user
from container import Container
from models import User, Response

app = Flask(__name__)
container = Container(os.getenv("SITEMAPS_INDEXING_ENVIRONMENT"))
app.config['SECRET_KEY'] = container.get_parameters().get('authentication')['secret_key']


@app.get("/urls")
@auth_required("ROLE_ADMIN")
def urls(current_user: User) -> tuple: # pylint: disable=unused-argument
    return (Response()).parse(), 200


@app.post("/sign_in")
def sign_in() -> tuple:
    try:
        token = authenticate_user(request.json, container.get_users_repository())

        if isinstance(token, dict):
            return (Response(data={"token": token})).parse(), 200

        return (Response(message="Could not sign in user")).parse(), 401
    except Exception as e:
        return (Response(message=str(e), error=str(e))).parse(), 401


@app.post("/sign_up")
def sign_up() -> tuple:
    try:
        if register_user(request.json, container.get_users_repository()) is True:
            return (Response()).parse(), 200

        return (Response(message="Could not sign up user")).parse(), 401
    except Exception as e:
        return (Response(message=str(e), error=str(e))).parse(), 500


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as exception:
        container.get_logger().critical(str(exception))
