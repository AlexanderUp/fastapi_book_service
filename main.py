from fastapi import FastAPI

from auth import auth_main
from routers import authors, books, publishers, users

app = FastAPI()

app.include_router(auth_main.auth_router)
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(publishers.router)
app.include_router(users.router)
