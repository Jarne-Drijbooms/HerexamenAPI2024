import crud
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_speler(db: Session, username: str, password: str):
    speler = crud.get_player_by_email(db, username)
    if not speler:
        return False
    if not verify_password(password, speler.hashed_password):
        return False
    return speler

def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default to 20 minutes of expiration time if ACCESS_TOKEN_EXPIRE_MINUTES variable is empty
        expire = datetime.utcnow() + timedelta(minutes=20)
    # Adding the JWT
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_player(db: Session, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate the credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    speler = crud.get_player_by_email(db, username)
    if speler is None:
        raise credentials_exception
    return speler

def get_current_active_speler(db: Session, token: str = Depends(oauth2_scheme)):
    current_speler = get_current_player(db, token)
    if not current_speler.is_active:
        raise HTTPException(status_code=400, detail="Inactive player")
    return current_speler