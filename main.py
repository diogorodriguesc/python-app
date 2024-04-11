from flask import Flask, request
from auth_middleware import auth_required, authenticate_user
from container import Container
import os
from models import User

app = Flask(__name__)
container = Container(os.getenv("SITEMAPS_INDEXING_ENVIRONMENT"))
app.config['SECRET_KEY'] = container.get_parameters().get('authentication')['secret_key']


@app.get("/urls")
@auth_required("ROLE_ADMIN")
def urls(current_user: User):
    if type(current_user) is User:
        return {

        }


@app.post("/authenticate")
def authenticate():
    try:
        return authenticate_user(request.json)
    except Exception as e:
        return {
            "message": str(e)
        }, 500


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as exception:
        container.get_logger().critical(str(exception))
