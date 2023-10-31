from .dependencies import router as transform_router, update_highlight_by_id
from .schemas import TextModel
from fastapi import Body, HTTPException
from pydantic import BaseModel
from ai.dependencies import chat_completion
from dependencies import humanize_now


@transform_router.post("/tldr")
async def transform_question(body: TextModel = Body(...)):
    text = body.text
    prompt = "tldr to one or two sentences this: " + text
    # call GPT-4 chat endpoint and await response
    text = await chat_completion(prompt, dry_run=body.dry_run)

    return {
        "text": text,
        "created_at": humanize_now() 
    }

@transform_router.post("/tldr/{id}")
async def transform_question_by_highlight_id(id: str, body: TextModel = Body(...)):
    highlight = await update_highlight_by_id(id, "tldr to one or two sentences this: {}", "/transform/tldr", body)
    return highlight

