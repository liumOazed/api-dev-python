import jwt 
from datetime import datetime, timedelta, timezone
from . import schemas, models
from sqlmodel import select
from .database import  SessionDep
from fastapi import Depends, status, HTTPException 
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") ## login is the endpoint of our url login

# We will need secret key which reside in our server
# Provide algo[HS 256]
# Expiration time

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define function
def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # this method will create the actual jwt tokens
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
# Now create a function to verify the token
# credentials_exception is saying what our exception should be if credentials doesn't match
def verify_access_token(token: str, credentials_exception): 
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM) # decode jwt
        id : str = str(payload.get("user_id")) # extract and cast id to string
        
        if id is None: 
            raise credentials_exception # throw error if no id
        token_data = schemas.TokenData(id=id) # Here we validate the token
    
    except jwt.PyJWTError:
        raise credentials_exception
    
    return token_data # return the token data so we can make use of it
    

# This function will take the token from the request and verify the token, extract id
def get_current_user(session: SessionDep,token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    # since token passing to the curent user we can pass it to verify_access_token
    token = verify_access_token(token, credentials_exception)
    user = session.exec(select(models.User).where(models.User.id == token.id)).first()
    
    return user
