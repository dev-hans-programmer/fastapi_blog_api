from fastapi import FastAPI

from src.routers.post import router as post_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Fast API"}


app.include_router(post_router, prefix="/posts")
