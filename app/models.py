from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
import sqlalchemy as sa
from typing import Optional

# sqlmodel/sqlalchemy model what database tables would look like
class Post(SQLModel, table=True):
    __tablename__ = "posts"
    
    id: int  = Field(index=True, primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True, nullable=False, sa_column_kwargs={"server_default": sa.text("TRUE")})
    created_at: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), 
                                                     nullable=False, server_default=sa.text("now()")))
    owner_id: int = Field(foreign_key="users.id", ondelete="CASCADE", nullable=False)
    owner: Optional["User"] = Relationship(back_populates="posts")
   

class User(SQLModel, table=True): 
    __tablename__ = "users"
    
    id: int  = Field(index=True, primary_key=True, nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True),
                                                     nullable=False, server_default=sa.text("now()")))
    posts: list[Post] = Relationship(back_populates="owner") 


class Vote(SQLModel, table=True):
    __tablename__ = "votes"
    
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE", primary_key=True, nullable=False)
    post_id: int = Field(foreign_key="posts.id", ondelete="CASCADE", primary_key=True, nullable=False)
    