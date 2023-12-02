from fastapi import FastAPI

from routers import authors, books, publishers

app = FastAPI()

app.include_router(authors.router)
app.include_router(books.router)
app.include_router(publishers.router)


@app.get('/')
async def root():
    return {'message': 'Hello Bigger Applications!'}