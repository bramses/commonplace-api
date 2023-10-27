from fastapi import HTTPException, Depends
from httpx import AsyncClient
from .schemas import Highlight, SourceType
import uuid

from .dependencies import router as ingest_router
from dependencies import get_client, get_host, humanize_now

@ingest_router.post("/highlight")
async def add_highlight(highlight: Highlight, client: AsyncClient = Depends(get_client)):

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
            print(res.json())
            highlight.transformations[idx] = {
                "error": f"Endpoint {get_host()}/transform/{transformation} returned status code {res.status_code} and error {res.json()['detail']}"
            }
        else:    
            highlight.transformations[idx] = {
                "endpoint": f"/transform/{transformation}",
                "version-history": [
                    {
                        "text": res.json()["text"],
                        "date": res.json()["date"]
                    }
                ],
                "name": f"{transformation}"
            }

    return processed_highlight
