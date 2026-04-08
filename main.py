from fastapi import FastAPI, Request, Form, Depends
from starlette.middleware.sessions import SessionMiddleware

from routers import auth, users, pages

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret")

app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(users.router)
