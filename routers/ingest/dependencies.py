from fastapi import APIRouter

router = APIRouter(
    prefix="/ingest",
    tags=["ingest"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)