from fastapi import APIRouter
from .schemas import Highlight, SourceType

router = APIRouter(
    prefix="/ingest",
    tags=["ingest"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

def convert_source_type_from_post_body(source_type, source_dict):
    print(source_dict)
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
    source_types = []
    if source_dict.get("book", None) is not None:
        source_types.append(SourceType.book)
    if source_dict.get("article", None) is not None:
        source_types.append(SourceType.article)
    if source_dict.get("video", None) is not None:
        source_types.append(SourceType.video)
    if source_dict.get("idea", None) is not None:
        source_types.append(SourceType.idea)

    return source_types