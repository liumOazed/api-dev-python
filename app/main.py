from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from typing import Optional
from random import randrange # will use it for id
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from app.database import create_db_and_tables, SessionDep
from . import models, schemas, utils    
from sqlmodel import select


app = FastAPI()

# Create tables on app startup
@app.on_event("startup") 
def on_startup():
    create_db_and_tables()
    print("Database tables created successfully.")

    
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', 
                                user='postgres', password='admin', cursor_factory=RealDictCursor) #RealDictCursor will give u the column names
        cursor = conn.cursor() # cursor will be used to execute sql statements
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)
    
    
my_posts = [{"title": "title of post 1", 
             "content": "content of post 1",
             "id":1},
            {"title": "favorite foods",
             "content": "I like pizza",
             "id":2}]

# Find a post by an id
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i # will give the specific index regarding that dictionary

# Path operation 
@app.get("/")
def root(): # keep it as descriptive as possible
    return {"message": "Welcome to FastAPI!"}


@app.get("/posts", response_model=list[schemas.PostResponse])
def get_posts(session: SessionDep):
    posts = session.exec(select(models.Post)).all()
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post:schemas.PostCreate, session: SessionDep): # referencing that Post pydantic and saving it as new_post
    # cursor.execute("""INSERT INTO  posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(
    #    post.title, post.content, post.published))
    # new_post = cursor.fetchone() # will return the new post (cursor.execute)
    # conn.commit() # push those changes
    
    new_post = models.Post(
        **post.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post
# title str, content str

# retrieving latest post
@app.get("/posts/latest", response_model=schemas.PostResponse)
def latest_post(session: SessionDep):
    # cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1 """)
    # posts = cursor.fetchone()
    latest_post = session.exec(select(models.Post).order_by(models.Post.created_at.desc()).limit(1)).first()
    # Check if a post exists
    if not latest_post:
        return {"message": "No posts found."}
    return latest_post

# retrieving one individual post

@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id:int, session: SessionDep):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    post = session.get(models.Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post 

# updating a post
@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id:int, post:schemas.PostCreate, session: SessionDep): # making sure the request comes in the right schema
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,(
    #     post.title, post.content, post.published, str(id))) 
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = session.get(models.Post, id)
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    update_data = post.model_dump(exclude_unset=True)  # Exclude fields not provided in the request
    for key, value in update_data.items():
        setattr(updated_post, key, value)  # Dynamically set attributes on the updated_post object
    session.commit()
    session.refresh(updated_post)
    return  updated_post

# deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, session: SessionDep):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone() # to get the deleted post
    # conn.commit()
    deleted_post = session.get(models.Post, id)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    session.delete(deleted_post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(session: SessionDep, user: schemas.UserCreate):
    # Before creating a new user, we need to create a hash for the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password # hashed the pass and stored it in user.pass
    
    new_user = models.User(
        **user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@app.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id:int, session: SessionDep):
    user = session.get(models.User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    return user 