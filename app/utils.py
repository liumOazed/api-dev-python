from passlib.context import CryptContext

# saying passlib what is the default algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

## This function is responsible for comparing 2 hashes. 
## It will take the raw pass hash it and compare the hashed pass in database

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)