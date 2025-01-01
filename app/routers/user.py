from .. import models, schemas, utils 
from fastapi import  status, HTTPException, APIRouter
from ..database import  SessionDep

router = APIRouter(
    prefix="/users"
)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
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

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id:int, session: SessionDep):
    user = session.get(models.User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    return user 