import jwt
from fastapi.exceptions import HTTPException
from datetime import datetime, timedelta, timezone

from conf.config import app_config


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, app_config.JWT_SECRET, algorithm=app_config.JWT_ALGORITHM
    )
    return encoded_jwt


credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
