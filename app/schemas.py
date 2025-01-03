from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# This pydantic model will represent what a post should look like

 # This also handles the direction of the users sending data to us  
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
# Now this will handle us the direction of data sending to users. PostResponse is responsible for sending the posts out

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    
# User Schema 
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
# Schema for token
class Token(BaseModel):
    access_token: str
    token_type: str
    
# Schema for token data that embedded in the token
class TokenData(BaseModel):
    id: Optional[str] = None