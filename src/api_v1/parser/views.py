import datetime
from typing import List, Any

from fastapi import APIRouter, Depends, UploadFile
from fastapi_cache.decorator import cache
from fastapi.responses import StreamingResponse

from src.alchemy.db_helper import *
from . import crud

from .schemas import ParseZamenaRequest, RemoveZamenaRequest

router = APIRouter(tags=["Parser"])

pass_ = os.environ.get("API_SECRET")


@router.get("/get_latest_zamena_link", response_model=dict)
@cache(300)
async def get_latest_zamena_link() -> dict:
    return await crud.get_latest_zamena_link()


@router.get("/get_founded_links", response_model=List[str])
@cache(300)
async def get_founded_links(session: AsyncSession = Depends(db_helper.session_dependency)) -> List[str]:
    return await crud.get_founded_links(session=session)


@router.get("/check_new")
async def check_new() -> dict[str, Any]:
    return await crud.check_new()


@router.get('/tasks', response_model=dict)
async def get_all_tasks() -> dict:
    return await crud.get_all_tasks()


@router.post("/parse_zamena", response_model=dict)
async def parse_zamena(request: ParseZamenaRequest) -> dict:
    return await crud.parse_zamena(request)


@router.post("/pdf2docx")
async def pdf2docx(docx: UploadFile):
    encoded_filename = f"attachment; filename=response.docx"
    output_stream = await crud.pdf2docx(docx)
    output_stream.seek(0)

    return StreamingResponse(
        output_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": encoded_filename}
    )


@router.get("/containers")
def get_containers():
    return crud.get_containers()


@router.delete("/zamena")
async def delete_zamena(request: RemoveZamenaRequest):
    return await crud.delete_zamena(request)


@router.post("/parse_group_schedule_v3")
async def parse_group_schedule_v3(file: UploadFile, monday_date: datetime.date):
    return await crud.parse_group_schedule_v3(file=file, monday_date=monday_date)
