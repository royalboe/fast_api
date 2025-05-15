from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from sqlmodel import select
from ..utils.dependencies import SessionDep, get_current_user
from ..schema import VoteBase
from ..models.votes import Vote

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_vote(vote: VoteBase, session: SessionDep, current_user=Depends(get_current_user)):
    
    statement = select(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id)

    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if (vote.dir == 1):
        if result:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already upvoted this post")
        session.add(vote)
        session.commit()

    return {"message": "Successfully upvoted post"}