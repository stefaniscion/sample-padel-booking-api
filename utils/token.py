from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "01f3e51c910ccac0de6f24850110ae436153e4d3a04f15713df5ff60193d26ad"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(user_id:int):
    to_encode = {"user": user_id}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def get_current_user(token:str):
    payload = jwt.decode(token, SECRET_KEY)
    user_id = payload.get("user")
    return user_id