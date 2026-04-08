from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from routers import auth, users, pages

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="secret")

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(pages.router)
