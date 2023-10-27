from fastapi import Depends, FastAPI


from dependencies import get_query_token, client
from routers.ingest.dependencies import router as ingest_router
from routers.transform.dependencies import router as transform_router

# idk why i need these imports but app breaks without them
import routers.ingest.highlight
import routers.transform.question
# end local imports


app = FastAPI()
app.include_router(ingest_router)
app.include_router(transform_router)

@app.on_event("shutdown")
async def shutdown():
    await client.aclose()

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
