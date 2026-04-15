from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from routers import auth, users, pages
import database

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="secret")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(pages.router)
app.include_router(database.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0")
