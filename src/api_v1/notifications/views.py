from fastapi import APIRouter

from src.api_v1.notifications import crud

router = APIRouter(tags=["Notifications"], include_in_schema=True)


@router.post("/send_single_message/")
async def send_single_message(token: str, session):
    return crud.send_single_message(session=session, token=token)
