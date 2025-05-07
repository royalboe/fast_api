from fastapi import FastAPI, HTTPException, status
from dotenv import load_dotenv
from sqlalchemy import text
from contextlib import asynccontextmanager

from .dependencies import SessionDep
from .database import create_db_and_tables
from .routes.post_routes import router as post_router
# from .routes.users_routes import router as user_router

load_dotenv()


# ---------------------------A-
# FastAPI Endpoints
# ----------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (if needed)

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health_check(session: SessionDep):
    try:
        session.exec(text('SELECT 1'))  # lightweight DB check
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}"
        )

@app.get("/")
def root():
    """
    Root route returns a simple welcome message.
    """
    return {"message": "Welcome to my API"}

# Include the routes

app.include_router(post_router, prefix="/api/posts", tags=["Posts"])
# app.include_router(user_router, prefix="/api/users", tags=["Users"])