from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers.auth.routers import router as auth_router
from app.routers.post.routers import router as post_router
from app.routers.blog.routers import router as blog_router


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth_router)
app.include_router(post_router)
app.include_router(blog_router)