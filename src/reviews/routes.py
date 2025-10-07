from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User
from .schema import ReviewCreateModel
from .service import ReviewService
from src.auth.dependencies import get_current_user
from src.db.main import get_session

review_router = APIRouter()


@review_router.post("/book/{book_uid}")
async def add_review(
    book_uid: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    new_review = await ReviewService.add_review(
        user_email=current_user.email,
        book_uid=book_uid,
        review_data=review_data,
        session=session,
    )

    return new_review
