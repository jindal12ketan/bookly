from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.books.schema import Book, BookCreateModal, BookUpdateModal
from src.db.main import get_session
from src.books.service import BookService
from src.auth.dependencies import AccessTokenBearer, RoleChecker

book_router = APIRouter()
book_service = BookService()

# Dependency instances
access_token_bearer = AccessTokenBearer()
# Allow both admin and user roles to access book routes
role_checker = Depends(RoleChecker(allowed_roles=["admin", "user"]))


@book_router.get(
    "/user/{user_uid}",
    response_model=List[Book],
    status_code=status.HTTP_200_OK,
    dependencies=[role_checker],
)
async def get_user_book_submissions(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
):
    """
    Retrieve all books submitted by a specific user.
    """

    books = await book_service.get_users_books(user_uid, session)
    return books


@book_router.get(
    "/",
    response_model=List[Book],
    status_code=status.HTTP_200_OK,
    dependencies=[role_checker],
)
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
):
    """
    Retrieve all books.
    """

    books = await book_service.get_all_books(session)
    return books


@book_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
    dependencies=[role_checker],
)
async def create_book(
    book_data: BookCreateModal,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
) -> dict:
    """
    Create a new book.
    """
    user_uid = token_details.get("user")["user_uid"]
    new_book = await book_service.create_book(
        book_data, user_uid=user_uid, session=session
    )
    return new_book


@book_router.get(
    "/{book_uid}",
    response_model=Book,
    status_code=status.HTTP_200_OK,
    dependencies=[role_checker],
)
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
) -> dict:
    """
    Retrieve a book by its UUID.
    """
    book = await book_service.get_book(book_uid, session)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return book


@book_router.patch(
    "/{book_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Book,
    dependencies=[role_checker],
)
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModal,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
) -> dict:
    """
    Update an existing book.
    """
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return updated_book


@book_router.delete(
    "/{book_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[role_checker],
)
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
):
    """
    Delete a book by its UUID.
    """
    book_to_delete = await book_service.delete_book(book_uid, session)
    if not book_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return None
