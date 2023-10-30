from fastapi import HTTPException, Depends
from httpx import AsyncClient
from .schemas import Highlight, SourceType, Source
import uuid
from log.gpterr import gpt_error
import asyncio

from log.dependencies import setup_logger
logger = setup_logger(__name__)

from .dependencies import router as ingest_router, derive_source_type_from_source, process_transformation
from dependencies import get_client, humanize_now
from ai.dependencies import embed_text


@ingest_router.post("/highlight")
async def add_highlight(highlight: Highlight, client: AsyncClient = Depends(get_client)):
    logger.debug(f"Received highlight: {highlight}.\n\nTransformations = {'None' if highlight.transformations is None else 'not None'}\nSource = {'None' if highlight.source is None else 'not None'}\nMargin Notes = {'None' if highlight.margin_notes is None else 'not None'}\n\n")

    if highlight.highlight is None or highlight.highlight == "":
        raise HTTPException(status_code=400, detail="Highlight cannot be empty")

    processed_highlight = {
        "highlight": highlight.highlight,
        "meta": {
            "source": highlight.source or None,
            "transformations": highlight.transformations or None,
            "margin_notes": highlight.margin_notes or None,
        },
        "vector": highlight.vector or None,
        "published": highlight.published or False,
        "created_at": humanize_now(),
        "updated_at": humanize_now(),
        "id": uuid.uuid4()
    }

    # call each transformation endpoint and await response and add to highlight
    if highlight.transformations is not None:
        tasks = [process_transformation(idx, transformation, highlight, client) for idx, transformation in enumerate(highlight.transformations)]
        processed_highlight["meta"]["transformations"] = await asyncio.gather(*tasks)
    
    if highlight.margin_notes is not None:
        processed_highlight["meta"]["margin_notes"] = [{"text": margin_note, "created_at": humanize_now()} for margin_note in highlight.margin_notes]


    if highlight.source is not None:
        source_dict = processed_highlight["meta"]["source"].dict()
        source_dict["category"] = derive_source_type_from_source(highlight.source.dict())
        processed_highlight["meta"]["source"] = Source(**source_dict)
    

    if highlight.vector is None:
        processed_highlight["vector"] = await embed_text(highlight.highlight)

    return processed_highlight