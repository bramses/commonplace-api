from fastapi import Request, Response
from fastapi.responses import HTMLResponse, StreamingResponse
from .dependencies import router as ingest_router
from dependencies import get_templates
from ai.dependencies import send_messages, arr_to_system_message
from typing import Generator
from log.dependencies import setup_logger
logger = setup_logger(__name__)
templates = get_templates()


@ingest_router.post("/chat")
async def chat_post(request: Request):
    messages = await request.json()
    messages = messages['messages']

    logger.debug("chat_post")
    logger.debug(messages)

    def event_stream() -> Generator[str, None, None]:
        for line in send_messages(messages=messages):
            text = line.choices[0].delta.get('content', '')
            if len(text): 
                yield text

    return StreamingResponse(event_stream(), media_type='text/event-stream')

@ingest_router.get("/chat")
async def chat_get(request: Request):
    logger.debug("chat_get")
    logger.debug(request)

    return templates.TemplateResponse("chat.html", {"request": request, "system_messages": arr_to_system_message(["You are a good listener that help your clients expand on a highlight. You ask questions that get the client to dive deeper into their margin note, suggesting creative directions.", "Rewrite the provided margin note given client input in first person at the end of every message with 'Here's the new margin note:'. Compile all the info from the conversation into the margin note, DO NOT leave important information from earlier drafts of margin notes behind. Keep mportant topics from previous drafts in your conversational memory and add them to the new margin note."])})


@ingest_router.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})