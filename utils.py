from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from users import users


SECRET_KEY = "this is a test"
ALGORITHIM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")




def get_user(obj):
    for p in users:
        if p["uname"] == obj.uname and p["password"] == obj.password:
             return p
        
def get_user_by_id(id):
    for p in users:
        if p["id"] == id:
            return p


def create_token(data: dict):
    data_encode = data.copy()
    encoded_data = jwt.encode(data_encode,SECRET_KEY,algorithm=ALGORITHIM)
    return encoded_data

def verify_access_token(token: str,credentials_exception):
    try:

        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHIM])
        id: str = payload.get("id")
        role: str = payload.get("role")
        if id is None:
            raise credentials_exception
        token_data = {"id":id,"role":role}
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"could not validate credentials",headers={"www-Authenticate":"Bearer"})
    return verify_access_token(token,credentials_exception)