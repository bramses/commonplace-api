from fastapi import APIRouter

router = APIRouter(
    prefix="/explore",
    tags=["explore"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

def craft_sql_query_from_filters():
    pass