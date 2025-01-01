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
from .routers import post, user

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

app.include_router(post.router)
app.include_router(user.router)
