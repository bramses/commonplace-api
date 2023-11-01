from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from dependencies import get_query_token, client
from routers.ingest.dependencies import router as ingest_router
from routers.transform.dependencies import router as transform_router
from routers.explore.dependencies import router as explore_router

# idk why i need these imports but app breaks without them
import routers.ingest.highlights
import routers.ingest.margin_notes
import routers.transform.questions
import routers.transform.tldr
import routers.transform.image
import routers.explore.highlights
# end local imports


app = FastAPI()
app.include_router(ingest_router)
app.include_router(transform_router)
app.include_router(explore_router)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("shutdown")
async def shutdown():
    await client.aclose()

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
