from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import db_helper
from src.api_v1.telegram_auth import crud
from src.api_v1.telegram_auth.schemas import (
    AuthDto,
    AuthRequest,
    AuthStatusDto,
    AuthStatusRequest,
    CreateStateDto,
)
from src.auth.auth import any_auth_method

router = APIRouter(tags=["telegram_auth"])


@router.post('/create_state', status_code = status.HTTP_201_CREATED)
async def create_state(session: AsyncSession = Depends(db_helper.session_dependency)) -> CreateStateDto:
    return await crud.create_state(session = session)


@router.post("/auth_status")
async def auth_status(request: AuthStatusRequest, session: AsyncSession = Depends(db_helper.session_dependency)) -> AuthStatusDto | None:
    return await crud.auth_status(request = request, session = session)


@router.post(
    "/verify_token",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(any_auth_method(roles=["Owner"]))]
)
async def verify_token(
    token: str = Form(...),
    user_id: str = Form(...),
    chat_id: str = Form(...),
    username: Optional[str] = Form(None),
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    photo_bytes: Optional[bytes] = None
    if photo is not None:
        photo_bytes = await photo.read()

    auth_request = AuthRequest(
        token=token,
        user_id=user_id,
        chat_id=chat_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        photo_bytes=photo_bytes
    )

    return await crud.verify_token(session=session, auth_request=auth_request)

