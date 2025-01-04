from typing import Annotated
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

# PostgreSQL connection details
db_name = "fastapi"
db_user = "postgres"
db_password = "admin"
db_host = "localhost"  # or the server IP
db_port = "5432"

postgres_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(postgres_url)

# Call create_db_and_tables() once to create the database tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
#Use get_session() whenever you need to perform database operations
def get_session():
    with Session(engine) as session:
        yield session

# Use SessionDep in FastAPI route handlers to automatically get a session without manual setup.
SessionDep = Annotated[Session, Depends(get_session)]


# Not needed but only for demo purposes if u wanna run raw sql in posgres library

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', 
#                                 user='postgres', password='admin', cursor_factory=RealDictCursor) #RealDictCursor will give u the column names
#         cursor = conn.cursor() # cursor will be used to execute sql statements
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ", error)
#         time.sleep(2)