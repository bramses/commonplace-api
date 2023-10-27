from fastapi import Depends, FastAPI

from dependencies import get_query_token
from routers.ingest import quote_real as quote

app = FastAPI()
app.include_router(quote.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
