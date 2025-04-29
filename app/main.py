from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import models
from .db.database import engine
from .routers import post, user, auth, vote
from .core.config import settings

############### Old Code: non graceful shutdown  ###############
# create the database tables if they don't exist (case of not using alembic)
# models.Base.metadata.create_all(bind=engine)

# app = FastAPI()

################ End Old Code #############


################### New Code: Lifespan Handler  ---> for graceful shutdown ###############################
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔌 Connecting to PostgreSQL...")
    try:
        # Create the database tables if they don't exist (case of not using alembic)
        # models.Base.metadata.create_all(bind=engine)
        print("✅ Connected.")
        yield
    finally:
        print("🧹 Closing PostgreSQL connection...")
        await engine.dispose()
        print("✅ Disconnected.")


# Create the FastAPI app with lifespan handler
app = FastAPI(lifespan=lifespan)

################ End of New Code #############


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}
