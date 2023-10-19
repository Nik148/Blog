from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.routers.auth.routers import router as auth_router
from app.routers.post.routers import router as post_router
from app.routers.blog.routers import router as blog_router


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.exception_handler(401)
async def handler_404(request: Request, exc):
    return RedirectResponse("/blog/login")

app.include_router(auth_router)
app.include_router(post_router)
app.include_router(blog_router)
