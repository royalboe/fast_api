from fastapi import FastAPI, HTTPException, status
from sqlalchemy import text
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from .utils.dependencies import SessionDep
from .routes.post_routes import router as post_router
from .routes.users_routes import router as user_router
from .routes.auth_routes import router as auth_router
from .routes.votes_routes import router as vote_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # create_db_and_tables()
    yield
    # Shutdown (if needed)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------A-
# FastAPI Endpoints
# ----------------------------

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
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(vote_router, prefix="/api/vote", tags=["Vote"])