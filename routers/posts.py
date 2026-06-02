from fastapi import FastAPI, HTTPException, Depends, APIRouter
from pydantic_model import user,response, vote_response
from fastapi.responses import JSONResponse
from fastapi import status
from typing import List, Optional
import oauth2
from database import engine, get_db
from fastapi.encoders import jsonable_encoder
import model_database
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
     tags=["posts"]
)



@router.post("/create_posts", status_code=201, response_model=response)
async def create_user(user: user, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
        # post_dict = user.model_dump()
        # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post_dict['title'], post_dict['content'], post_dict['published']))
        # created_post=cursor.fetchone()
        # conn.commit()
       user=user.model_dump()
       user["user_id"] = user_id
       new_post=model_database.Post(**user)
       db.add(new_post)
       db.commit()
       db.refresh(new_post) 
       return new_post

@router.get("/get_posts", status_code=200, response_model=List[vote_response])
async def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int =10,
                    skip: int =0, search: Optional[str] = ""):
        # cursor.execute("""SELECT * FROM posts""")
        # myposts=cursor.fetchall()
        # print(myposts)
        # myposts=db.query(model_database.Post).filter(model_database.Post.title.contains(search)).limit(limit).offset(skip).all()
        my_posts=db.query(model_database.Post, func.count(model_database.Votes.post_id).label("votes")).join(model_database.Votes, model_database.Post.id==model_database.Votes.post_id, isouter=True).group_by(model_database.Post.id).filter(model_database.Post.title.contains(search)).limit(limit).offset(skip).all()
        return my_posts

@router.get("/get_posts/latest_post", response_model=vote_response, status_code=200)
async def get_latest_post(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
    # latest_post=cursor.fetchone()
    # latest_post=db.query(model_database.Post).order_by(model_database.Post.id.desc()).limit(1).first()
    latest_post=db.query(model_database.Post, func.count(model_database.Votes.post_id).label("votes")).join(model_database.Votes, model_database.Post.id==model_database.Votes.post_id, isouter=True).group_by(model_database.Post.id).order_by(model_database.Post.id.desc()).limit(1).first()
    return latest_post

@router.get("/get_posts/{post_id}", status_code=200, response_model=vote_response)
async def get_post(post_id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,))
    # post=cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {post_id} was not found")
    post=db.query(model_database.Post, func.count(model_database.Votes.post_id).label("votes")).join(model_database.Votes, model_database.Post.id==model_database.Votes.post_id, isouter=True).group_by(model_database.Post.id).filter(model_database.Post.id==post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {post_id} was not found")
    return post

@router.delete("/delete_post/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (post_id,))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    # if deleted_post:
    #     return JSONResponse(status_code=200, content={"message": "post deleted successfully"})
    del_post=db.query(model_database.Post).filter(model_database.Post.id==post_id).first()
    if del_post:
        if del_post.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        db.delete(del_post)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "post deleted successfully"})
    return JSONResponse(status_code=404, content={"message": "post not found"})

@router.put("/update_post/{post_id}")
async def update_post(post: user, post_id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, post_id))
    # updated_post=cursor.fetchone()
    # conn.commit()
    # if updated_post:
    #     return JSONResponse(status_code=200, content=jsonable_encoder({"message": "post updated successfully", "post": updated_post}))
    update_query=db.query(model_database.Post).filter(model_database.Post.id==post_id)
    updated_post=update_query.first()
    if updated_post:
        if updated_post.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        update_query.update(post.model_dump(), synchronize_session=False)
        db.commit()
        return JSONResponse(status_code=200, content=jsonable_encoder({"message": "post updated successfully", "post": updated_post}))
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {post_id} does not exist")
        