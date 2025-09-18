from fastapi import APIRouter, status, HTTPException, Depends
from .schema import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import create_access_token, decode_access_token, verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse

auth_router = APIRouter()

user_service = UserService()

REFRESH_TOKEN_EXPIRY = timedelta(days=30)  # 30 days in time delta format


@auth_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_Account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session=session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User already exists"
        )
    new_user = await user_service.create_user(user_data, session=session)
    return new_user


@auth_router.post("/login")
async def login_user(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password
    user = await user_service.get_user_by_email(email, session=session)
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)}
            )
            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                expiry=REFRESH_TOKEN_EXPIRY,
                refresh=True,
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "user_uid": str(user.uid),
                    },
                },
            )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
    )
