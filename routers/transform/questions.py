from .dependencies import router as transform_router, update_highlight_by_id
from dependencies import humanize_now
from fastapi import Body
from pydantic import BaseModel
from ai.dependencies import chat_completion

class TextModel(BaseModel):
    text: str


@transform_router.post("/question")
async def transform_question(body: TextModel = Body(...)):
    text = body.text
    # call GPT-4 chat endpoint and await response
    prompt = f'''Generate a single question from this quote.
The end user cannot see the quote so DO NOT use any abstract concepts like \"the speaker\" or \"the writer\" in your question. BE EXPLICIT. DO NOT ASSUME the reader has read the quote.
DO NOT use passive voice and do not use passive pronouns like he/she/they/him/her etc.
You can use any of who/what/where/when/why.
Say nothing else.\n\nQuote:\n\n{text}\n\nQ:'''
    text = await chat_completion(prompt)

    print(text)
    return {
        "text": text,
        "created_at": humanize_now() 
    }

@transform_router.post("/question/{id}")
async def transform_question_by_highlight_id(id: str, body: TextModel = Body(...)):
    highlight = await update_highlight_by_id(id, '''Generate a single question from this quote.
The end user cannot see the quote so DO NOT use any abstract concepts like \"the speaker\" or \"the writer\" in your question. BE EXPLICIT. DO NOT ASSUME the reader has read the quote.
DO NOT use passive voice and do not use passive pronouns like he/she/they/him/her etc.
You can use any of who/what/where/when/why.
Say nothing else.\n\nQuote:\n\n{}\n\nQ:''' , "/transform/tldr", body)
    return highlight