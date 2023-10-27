from fastapi import FastAPI,status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from fastapi import Depends,status,HTTPException
import utils
import models





pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")








app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.get("/",status_code=status.HTTP_200_OK)
def root():
    return {"message": "Welcome to the test api"}

@app.post("/login",status_code=status.HTTP_200_OK)
def login(payload:models.User):
    cred = (models.User(**payload.model_dump()))
    user = utils.get_user(cred)
    #hashed_pwd = pwd_context.hash(payload.password)
    
    if not user:
        raise HTTPException(status_code =status.HTTP_401_UNAUTHORIZED,detail ="Invalid username or password")
    else: 
        access_token = utils.create_token(data={"id":user["id"],"role":user["role"]})
        return {"access_token":access_token,"token_type":"bearer"}
  
@app.get("/dashboard/{id}")
def user_dashboard(user_id: int = Depends(utils.get_current_user)):
    print(user_id)
    user = utils.get_current_user(user_id)
    return user

   
   
             
             
#if __name__ == '__main__':
    #uvicorn.run("main:app", host="0.0.0.0", port=8036, reload=True)
   