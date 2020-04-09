from db import db

import hashlib
import jwt
from bson import ObjectId

SECRET = "TESTSECRET"
ALGORITHM = "HS256"


async def validate_register_data(data: dict) -> bool:
    try:
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
    except KeyError:
        return False

    if len(username) < 4 or " " in username or await db().users.find_one({'username': username.lower()}):
        return False

    if len(password1) < 6 or " " in password1 or password1 != password2:
        return False
    return True


async def hash_pass(password: str) -> str:
    global SECRET
    hashed_pass = hashlib.sha512(
        password.encode() + SECRET.encode(),
    ).hexdigest()
    return hashed_pass


async def verify_user(data: dict) -> tuple:
    username = data['username'].lower()
    password = data['password']
    db_user = await db().users.find_one({"username": username})
    if not db_user:
        return {"message": "User does not exists"}, 404
    if await compare_password(password, db_user['password']):
        return {"message": await generate_token(db_user)}, 200
    else:
        return {"message": "Wrong password"}, 400


async def compare_password(password: str, user_password: str) -> bool:
    return await hash_pass(password) == user_password


async def generate_token(data: dict) -> str:
    payload = {
        'username': data['username'],
        '_id': str(data['_id'])
    }
    return jwt.encode(payload, SECRET, ALGORITHM).decode()


async def iterable_objects_object_id_to_str(iterable: list) -> list:
    for el in iterable:
        for key, value in el.items():
            if isinstance(value, ObjectId):
                el[key] = str(value)
    return iterable
