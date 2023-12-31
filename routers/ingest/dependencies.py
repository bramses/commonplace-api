from fastapi import APIRouter
from .schemas import SourceType
from dependencies import get_host


router = APIRouter(
    prefix="/ingest",
    tags=["ingest"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

def convert_source_type_from_post_body(source_type, source_dict):
    if source_type == SourceType.book:
        return {
            "book": {
                "title": source_dict.get("title", None),
                "author": source_dict.get("author", None),
                "page": source_dict.get("page", None),
                "url": source_dict.get("url", None)
            }
        }
    elif source_type == SourceType.article:
        return {
            "article": {
                "title": source_dict.get("title", None),
                "author": source_dict.get("author", None),
                "anchor": source_dict.get("anchor", None),
                "url": source_dict.get("url", None)
            }
        }
    elif source_type == SourceType.video:
        return {
            "video": {
                "title": source_dict.get("title", None),
                "timestamp": source_dict.get("timestamp", None),
                "url": source_dict.get("url", None)
            }
        }
    elif source_type == SourceType.idea:
        return {
            "idea": {
                "context": source_dict.get("context", None),
                "url": source_dict.get("url", None)
            }
        }
    else:
        return None
    
def derive_source_type_from_source(source_dict):
    source_type = None
    if source_dict.get("book", None) is not None:
        source_type = (SourceType.book.value)
    if source_dict.get("article", None) is not None:
        source_type = (SourceType.article.value)
    if source_dict.get("video", None) is not None:
        source_type = (SourceType.video.value)
    if source_dict.get("idea", None) is not None:
        source_type = (SourceType.idea.value)

    return source_type


async def process_transformation(idx, transformation, highlight, client):
    res = await client.post(f"{get_host()}/transform/{transformation}", json={"text": highlight.highlight}, headers={"Content-Type": "application/json"}, timeout=30)
    if res.status_code == 404:
        return {
            "error": f"Endpoint {get_host()}/transform/{transformation} not found"
        }
    elif res.status_code != 200:
        return {
            "error": f"Endpoint {get_host()}/transform/{transformation} returned status code {res.status_code} and error {res.json()['detail']}"
        }
    else:    
        return {
            "endpoint": f"/transform/{transformation}",
            "version_history": [
                {
                    "text": res.json()["text"],
                    "created_at": res.json()["created_at"]
                }
            ],
            "name": f"{transformation}"
        }