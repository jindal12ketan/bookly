from fastapi import APIRouter, status, HTTPException, Depends
from src.db.redis import add_jti_to_blocklist
from .schema import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import create_access_token, verify_password
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from .models import User

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(allowed_roles=["admin", "user"])


REFRESH_TOKEN_EXPIRY = timedelta(days=30)


@auth_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    existing = await user_service.user_exists(user_data.email, session=session)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    try:
        new_user = await user_service.create_user(user_data, session=session)
        return new_user
    except Exception:
        await session.rollback()
        raise


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    user = await user_service.get_user_by_email(login_data.email, session=session)
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )
    access_token = create_access_token(
        user_data={"email": user.email, "user_uid": str(user.uid), "role": user.role}
    )
    refresh_token = create_access_token(
        user_data={"email": user.email, "user_uid": str(user.uid), "role": user.role},
        expiry=REFRESH_TOKEN_EXPIRY,
        refresh=True,
    )
    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {"email": user.email, "user_uid": str(user.uid)},
    }


@auth_router.get("/refresh-token", status_code=status.HTTP_200_OK)
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):

    exp_ts = token_details.get("exp")
    if not exp_ts or datetime.fromtimestamp(exp_ts) <= datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token"
        )
    user_payload = token_details.get("user")
    if not user_payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Malformed token"
        )
    new_access_token = create_access_token(user_data=user_payload)
    return {"access_token": new_access_token}


@auth_router.get("/logout", status_code=status.HTTP_200_OK)
async def logout_user(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]
    await add_jti_to_blocklist(jti)
    return {"message": "Logged out successfully"}


@auth_router.get("/me", response_model=UserModel, status_code=status.HTTP_200_OK)
async def get_current_user(
    user: User = Depends(get_current_user), _: bool = Depends(role_checker)
):

    return user
