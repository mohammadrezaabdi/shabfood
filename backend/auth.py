import time
import os
import binascii
import jwt
from typing import Dict
from enum import Enum
from fastapi import Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

JWT_SECRET = binascii.hexlify(os.urandom(32))
JWT_ALGORITHM = "HS256"
JWT_EXPIRATIN = 60  # min

signed_users = dict()


class User_type(str, Enum):
    customer = "Customer"
    deliverer = "Deliverer"
    restaurant = "Restaurant"


def token_response(token: str, user_type: User_type):
    return {
        "access_token": token,
        "token_type": "Bearer",
        "object_type": user_type
    }


def create_token(id: str, user_type: User_type) -> Dict[str, str]:
    payload = {
        "id": id,
        "user_type": user_type,
        "expires": time.time() + 60 * JWT_EXPIRATIN
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    signed_users[id] = (user_type, token)
    return token_response(token, user_type)


def get_current_active_user(token: str, user_type: User_type) -> str:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = decoded_token.get("id")
        if user_id is None or user_id not in signed_users or (user_type, token) != signed_users[user_id]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code.")
        if decoded_token.get("expires") < time.time():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Expired token.")
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials.")
    return user_id


class JWTBearer(HTTPBearer):
    def __init__(self, user_type: User_type, auto_error: bool = True):
        self.user_type = user_type
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme.")
            return get_current_active_user(credentials.credentials, self.user_type)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code.")
