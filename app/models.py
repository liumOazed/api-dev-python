from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
import sqlalchemy as sa

# sqlmodel/sqlalchemy model what database tables would look like
class Post(SQLModel, table=True):
    __tablename__ = "posts"
    
    id: int  = Field(index=True, primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True, nullable=False, sa_column_kwargs={"server_default": sa.text("TRUE")})
    created_at: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), 
                                                     nullable=False, server_default=sa.text("now()")))
   

class User(SQLModel, table=True): 
    __tablename__ = "users"
    
    id: int  = Field(index=True, primary_key=True, nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True),
                                                     nullable=False, server_default=sa.text("now()")))
    