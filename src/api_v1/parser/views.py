import datetime
import os
from typing import List, Any
from fastapi import APIRouter, Depends, UploadFile
from fastapi_cache.decorator import cache
from fastapi.responses import StreamingResponse
from celery.result import AsyncResult
from src.alchemy.db_helper import db_helper, AsyncSession
from . import crud

from .schemas import ParseZamenaJsonRequest, ParseZamenaRequest, RemoveZamenaRequest

router = APIRouter(tags=["Parser"])

pass_: str = os.environ["API_SECRET"]


@router.get("/get_latest_zamena_link", response_model=dict)
# @cache(300)
async def get_latest_zamena_link() -> dict:
    return await crud.get_latest_zamena_link()


@router.get("/get_founded_links", response_model=List[str])
@cache(300)
async def get_founded_links(session: AsyncSession = Depends(db_helper.session_dependency)) -> List[str]:
    return await crud.get_founded_links(session=session)


@router.get("/check_new")
async def check_new() -> dict[str, Any]:
    return await crud.check_new()


@router.get('/tasks', response_model = dict)
def get_all_tasks() -> dict:
    return crud.get_all_tasks()


@router.post("/parse_zamena", response_model=dict)
async def parse_zamena(request: ParseZamenaRequest) -> dict:
    return await crud.parse_zamena(request)


@router.post('/parse_zamena_json', response_model = dict)
def parse_zamena_json(request: ParseZamenaJsonRequest) -> dict:
    return crud.parse_zamena_json(request = request)


@router.get("/status")
def status(task_id: str) -> dict:
    r: AsyncResult = crud.tasks.parser_celery_app.AsyncResult(task_id)
    return {
        'id': r.id,
        'status': r.status,
        'result': r.traceback if r.failed() else r.result,
    }


@router.post("/pdf2docx")
async def pdf2docx(docx: UploadFile):
    encoded_filename = "attachment; filename=response.docx"
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
