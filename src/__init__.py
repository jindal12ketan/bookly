from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is Starting")
    await init_db()
    yield
    print("Server is Stopped")


version = "v1"

app = FastAPI(
    title="Bookly",
    description="Rest API for books review services",
    version=version,
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
