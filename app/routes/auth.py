from fastapi import APIRouter, HTTPException, status, Response
from ..utils.dependencies import SessionDep

router = APIRouter()

@router.post("/login")
def login(session: SessionDep):
    
    return {"message": "Hello from login"}