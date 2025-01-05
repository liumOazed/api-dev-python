from .. import models, schemas, oauth2
from fastapi import  status, HTTPException, APIRouter, Depends
from ..database import  SessionDep
from sqlmodel import select


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(session: SessionDep, vote: schemas.Vote, current_user: int = Depends(oauth2.get_current_user)):
    
    post = session.exec(select(models.Post).where(models.Post.id == vote.post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} does not exist")
    
    # Construct the query
    vote_query = select(models.Vote).where(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id
    )
    
    # Execute the query and get the first result
    found_vote = session.exec(vote_query).first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        session.add(new_vote)
        session.commit()
        return {"message": "Successfully added vote"}
        
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        # Delete the vote
        session.delete(found_vote)
        session.commit()
        return {"message": "Successfully deleted vote"}