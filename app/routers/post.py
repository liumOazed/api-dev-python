from .. import models, schemas, oauth2
from fastapi import Depends, Response, status, HTTPException, APIRouter
from ..database import  SessionDep
from sqlmodel import select, func
from typing import Optional


router = APIRouter(
    prefix="/posts",
    tags=["Posts"] 
)



@router.get("/", response_model=list[schemas.PostOut])
def get_posts(session: SessionDep, current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # print(search)
    # query = select(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip) # Apply the limit to the query plus skip
    # posts = session.exec(query).all() # Execute the query and fetch results
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # Count votes and label it as "likes"
    joined_query = select(models.Post, func.count(models.Vote.post_id).label("likes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip) # LEFT JOIN votes ON posts.id = votes.post_id
    
    # Execute the query
    results = session.exec(joined_query).all()
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post:schemas.PostCreate, session: SessionDep, current_user: int = Depends(oauth2.get_current_user)): # referencing that Post pydantic and saving it as new_post
    # cursor.execute("""INSERT INTO  posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(
    #    post.title, post.content, post.published))
    # new_post = cursor.fetchone() # will return the new post (cursor.execute)
    # conn.commit() # push those changes
    # print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, 
        **post.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post
# title str, content str

# retrieving latest post
@router.get("/latest", response_model=schemas.PostOut)
def latest_post(session: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1 """)
    # posts = cursor.fetchone()
    joined_query = select(models.Post, func.count(models.Vote.post_id).label("likes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
    ).group_by(models.Post.id).order_by(models.Post.created_at.desc()).limit(1)
    latest_post = session.exec(joined_query).first()
    # Check if a post exists
    if not latest_post:
        return {"message": "No posts found."}
    return latest_post

# retrieving one individual post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, session: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    # post = session.get(models.Post, id)
    joined_query = select(models.Post, func.count(models.Vote.post_id).label("likes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
    ).where(models.Post.id == id).group_by(models.Post.id)
    post = session.exec(joined_query).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post

# updating a post
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id:int, post:schemas.PostCreate, session: SessionDep, current_user: int = Depends(oauth2.get_current_user)): # making sure the request comes in the right schema
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,(
    #     post.title, post.content, post.published, str(id))) 
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = session.get(models.Post, id)
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to perform requested action")
    
    update_data = post.model_dump(exclude_unset=True)  # Exclude fields not provided in the request
    for key, value in update_data.items():
        setattr(updated_post, key, value)  # Dynamically set attributes on the updated_post object
    session.commit()
    session.refresh(updated_post)
    return  updated_post

# deleting a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, session: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone() # to get the deleted post
    # conn.commit()
    deleted_post = session.get(models.Post, id)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to perform requested action")
    
    session.delete(deleted_post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)