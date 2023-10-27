from fastapi import APIRouter

router = APIRouter(
    prefix="/explore",
    tags=["explore"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)