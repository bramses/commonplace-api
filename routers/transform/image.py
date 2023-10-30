

from .dependencies import router as transform_router
from dependencies import humanize_now
from fastapi import Body
from pydantic import BaseModel
from ai.dependencies import chat_completion, image_completion
from images.dependencies import dalle_img_to_cf

class TextModel(BaseModel):
    text: str


@transform_router.post("/image")
async def transform_question(body: TextModel = Body(...)):
    text = body.text
    pre_prompt = f"Summarize the following into a theme and create an art prompt from the feel of the text aesthetically along the lines of: 'an abstract of [some unique lesser known art style from history] version of {text}' where x is the feel of the text aesthetically. Remove any unsafe or NSFW content. Just return the art prompt, say nothing else."
    # call GPT-4 chat endpoint and await response
    text = await chat_completion(pre_prompt)

    image_url = await image_completion(text)
    cf_url = await dalle_img_to_cf(image_url)

    return {
        "text": cf_url,
        "created_at": humanize_now() 
    }