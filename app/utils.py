from passlib.context import CryptContext

# saying passlib what is the default algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)