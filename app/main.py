from fastapi import FastAPI


from app.users.router import router as router_users
from app.fandoms.router import router as router_fandoms
from app.fics.router import router as router_fics
from app.comments.router import router as router_comments
from app import general_get_router

from app.db import Base, engine
from app.users.models import Users
from app.fandoms.models import Fandoms
from app.fics.models import Fics
from app.comments.models import Comments

app = FastAPI()

app.include_router(general_get_router.router)
app.include_router(router_users)
app.include_router(router_fandoms)
app.include_router(router_fics)

app.include_router(router_comments)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("shutdown")
async def on_shutdown():
    await engine.dispose()