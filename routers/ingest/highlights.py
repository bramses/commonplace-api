from fastapi import HTTPException, Depends
from httpx import AsyncClient
from .schemas import Highlight, SourceType, Source
import uuid

from log.dependencies import setup_logger
logger = setup_logger(__name__)

from .dependencies import router as ingest_router, convert_source_type_from_post_body, derive_source_type_from_source
from dependencies import get_client, get_host, humanize_now

@ingest_router.post("/highlight")
async def add_highlight(highlight: Highlight, client: AsyncClient = Depends(get_client)):
    logger.debug(f"Received highlight: {highlight}.\n\nTransformations = {'None' if highlight.transformations is None else 'not None'}\nSource = {'None' if highlight.source is None else 'not None'}\nMargin Notes = {'None' if highlight.margin_notes is None else 'not None'}\n\n")

    if highlight.highlight is None:
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
    for idx, transformation in enumerate(highlight.transformations):
        res = await client.post(f"{get_host()}/transform/{transformation}", json={"text": highlight.highlight}, headers={"Content-Type": "application/json"})
        if res.status_code == 404:
            highlight.transformations[idx] = {
                "error": f"Endpoint {get_host()}/transform/{transformation} not found"
            }
        elif res.status_code != 200 and res.status_code != 404:
            highlight.transformations[idx] = {
                "error": f"Endpoint {get_host()}/transform/{transformation} returned status code {res.status_code} and error {res.json()['detail']}"
            }
        else:    
            highlight.transformations[idx] = {
                "endpoint": f"/transform/{transformation}",
                "version-history": [
                    {
                        "text": res.json()["text"],
                        "created_at": res.json()["created_at"]
                    }
                ],
                "name": f"{transformation}"
            }
    
    if highlight.margin_notes is not None:
        processed_highlight["meta"]["margin_notes"] = [{"text": margin_note, "created_at": humanize_now()} for margin_note in highlight.margin_notes]


    if highlight.source is not None:
        source_dict = processed_highlight["meta"]["source"].dict()
        source_dict["category"] = derive_source_type_from_source(highlight.source.dict())
        processed_highlight["meta"]["source"] = Source(**source_dict)
    


    return processed_highlight