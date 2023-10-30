from .dependencies import router as transform_router
from dependencies import humanize_now
from fastapi import Body
from pydantic import BaseModel
from ai.dependencies import chat_completion

class TextModel(BaseModel):
    text: str


@transform_router.post("/tldr")
async def transform_question(body: TextModel = Body(...)):
    text = body.text
    prompt = "tldr to one or two sentences this: " + text
    # call GPT-4 chat endpoint and await response
    text = await chat_completion(prompt)

    print(text)
    return {
        "text": text,
        "created_at": humanize_now() 
    }