from .dependencies import router as transform_router
from dependencies import humanize_now
from fastapi import Body
from pydantic import BaseModel

class TextModel(BaseModel):
    text: str


@transform_router.post("/question")
async def transform_question(body: TextModel = Body(...)):
    text = body.text
    print("transforming question" + text)
    return {
        "text": "transformed question: " + text,
        "created_at": humanize_now() 
    }