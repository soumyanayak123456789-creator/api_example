from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import model_database
import oauth2
from pydantic_model import vote
router=APIRouter(
    tags=["Vote"]
)

@router.post("/vote", status_code=status.HTTP_201_CREATED)
async def vote(vote: vote, db: Session=Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_exist=db.query(model_database.Post).filter(model_database.Post.id==vote.post_id).first()
    if not post_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} does not exist")
    vote_query=db.query(model_database.Votes).filter(model_database.Votes.post_id==vote.post_id, model_database.Votes.user_id==user_id)
    found_vote=vote_query.first()
    if vote.dir==1:
        if not found_vote:
            new_vote=model_database.Votes(post_id=vote.post_id,user_id=user_id)
            db.add(new_vote)
            db.commit()
            return {"message": "vote added successfully"}
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user has already voted on the post")
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="vote does not exist")
        db.delete(found_vote)
        db.commit()
        return {"message": "vote deleted successfully"}