import jwt
from functools import wraps
from urllib import request
from flask import request, abort, current_app
from models import User
from repository.users_repository import UsersRepository
import hashlib


def auth_required(role: str, users_repository: UsersRepository):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None

            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]
            if not token:
                return {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401

            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = User(data["user_id"], data['role'])
                if current_user is None:
                    return {
                        "message": "Invalid Authentication token!",
                        "data": None,
                        "error": "Unauthorized"
                    }, 401
                if type(current_user) is User and current_user.get_role() != role:
                    abort(403)
            except Exception as e:
                return {
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e)
                }, 500

            return f(current_user, *args, **kwargs)
        return decorated_function
    return decorator


def authenticate_user(params: dict, users_repository: UsersRepository) -> dict:
    if type(params) is not dict or params.keys() != {'user', 'password'}:
        raise Exception("Body params invalid")

    user = users_repository.checkIfExists(params['user'], hashlib.sha256(params['password'].encode("utf-8")).hexdigest())
    if not user:
        raise Exception("Invalid credentials")

    token = jwt.encode({'user_id': user[0], 'role': 'ROLE_ADMIN'}, current_app.config['SECRET_KEY'], algorithm='HS256')

    return {
        'token': token
    }


def register_user(params: dict, users_repository: UsersRepository) -> dict:
    if type(params) is not dict or params.keys() != {'user', 'password', 'role'}:
        raise Exception("Body params invalid")

    users_repository.create_user(
        params["user"],
        hashlib.sha256(params['password'].encode("utf-8")).hexdigest(),
        params["role"]
    )

    return {

    }
