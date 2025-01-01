from fastapi import APIRouter, status, HTTPException, Depends
from ..database import  SessionDep
from .. import schemas, models, utils, oauth2
from sqlmodel import select
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login")
def login(session: SessionDep, user_credentials: OAuth2PasswordRequestForm = Depends()):
    
    user = session.exec(
        select(models.User).where(models.User.email == user_credentials.username)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )
        
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Now create and return token
    access_token = oauth2.create_access_token(data={"user_id": user.id}) #payload
    return {"access_token": access_token, "token_type": "bearer"}
    
    