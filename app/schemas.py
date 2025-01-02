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

# Now this will handle us the direction of data sending to users

class PostResponse(PostBase):
    # id: int
    created_at: datetime
    
# User Schema 
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    
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