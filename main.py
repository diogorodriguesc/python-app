import os

from auth_middleware import auth_required, authenticate_user, register_user
from container import Container
from flask import Flask, request
from models import User, Response

app = Flask(__name__)
container = Container(os.getenv("SITEMAPS_INDEXING_ENVIRONMENT"))
app.config['SECRET_KEY'] = container.get_parameters().get('authentication')['secret_key']


@app.get("/urls")
@auth_required("ROLE_ADMIN")
def urls(current_user: User):
    if type(current_user) is User:
        return (Response()).parse(), 200


@app.post("/sign_in")
def sign_in():
    try:
        token = authenticate_user(request.json, container.get_users_repository())
        if token:
            return (Response(data={"token": token})).parse(), 200
    except Exception as e:
        return (Response(message=str(e), error=str(e))).parse(), 500


@app.post("/sign_up")
def sign_up():
    try:
        if register_user(request.json, container.get_users_repository()) is True:
            return (Response()).parse(), 200
    except Exception as e:
        return (Response(message=str(e), error=str(e))).parse(), 500


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as exception:
        container.get_logger().critical(str(exception))
