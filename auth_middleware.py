from functools import wraps
import hashlib

import jwt

from flask import request, abort, current_app
from models import User
from repositories import UsersRepository


def auth_required(role: str):
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
                if isinstance(current_user, User) and current_user.get_role() != role:
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


def authenticate_user(params: dict, users_repository: UsersRepository) -> str:
    if not isinstance(params, dict) or params.keys() != {'user', 'password'}:
        raise Exception("Body params invalid")

    user = users_repository.checkIfExists(params['user'], create_password_hash(params["password"]))
    if not user:
        raise Exception("Invalid credentials")

    token = jwt.encode({'user_id': user[0], 'role': 'ROLE_ADMIN'}, current_app.config['SECRET_KEY'], algorithm='HS256')

    return token


def register_user(params: dict, users_repository: UsersRepository) -> bool:
    if not isinstance(params, dict) or params.keys() != {'user', 'password'}:
        raise Exception("Body params invalid")

    users_repository.create_user(
        params["user"],
        create_password_hash(params["password"]),
        "ROLE_ADMIN"
    )

    return True


def create_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
