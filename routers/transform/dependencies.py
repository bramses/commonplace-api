from fastapi import APIRouter


router = APIRouter(
    prefix="/transform",
    tags=["transform"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)