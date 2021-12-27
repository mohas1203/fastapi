from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from app import models, schemas
from app.database import get_db
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer("login")

SECRETY_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_min


# Function to create access token
def create_access_token(data: dict, ):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRETY_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# Function to very access token
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRETY_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("user_id")

        if not user_id:
            raise credentials_exception

        token_data = schemas.TokenData(id=user_id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="could not validate credentials", headers={"WWW-Authenticate": "Bearer"}
                                          )

    jwt_token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == jwt_token.id).first()
    return user
