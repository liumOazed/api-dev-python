from fastapi import FastAPI
from app.database import create_db_and_tables
from .routers import post, user, auth

app = FastAPI()

# Create tables on app startup
@app.on_event("startup") 
def on_startup():
    create_db_and_tables()
    print("Database tables created successfully.")



# Path operation 
# @app.get("/")
# def root(): # keep it as descriptive as possible
#     return {"message": "Welcome to FastAPI!"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)