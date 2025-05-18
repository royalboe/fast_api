from fastapi import HTTPException, Depends, APIRouter, status
from sqlmodel import select
from ..utils.oauth2 import get_current_user
from ..utils.dependencies import SessionDep
from ..schema.schema import VoteBase
from ..models.votes import Vote
from ..models.post import Post as PostModel

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_vote(vote: VoteBase, session: SessionDep, current_user=Depends(get_current_user)):
    post = session.get(PostModel, vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    statement = select(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id)

    result = session.exec(statement).first()
    # if not result:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if (vote.dir == 1):
        if result:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already upvoted this post")
        new_vote = Vote(user_id = current_user.id, post_id= vote.post_id)
        session.add(new_vote)
        session.commit()
        session.refresh(new_vote)
        return {"message": "Successfully upvoted post"}
    else:
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        session.delete(result)
        session.commit()
        return {"message": "Successfully downvoted post."}

    