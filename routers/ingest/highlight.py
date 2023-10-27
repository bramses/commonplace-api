from fastapi import HTTPException, Depends
from httpx import AsyncClient
from .schemas import Highlight, SourceType

from .dependencies import router as ingest_router
from dependencies import get_client


'''
add highlight to db
highlight schema example:
{
    "highlight": "string", # required
    "meta": {
        "source": {
            "url": "string", # optional
            "book": {
                "title": "string",
                "author": "string",
                "page": "string"
            },
            "article": {
                "title": "string",
                "author": "string",
                "anchor": "string"
            },
            "video": {
                "title": "string",
                "author": "string",
                "timestamp": "string"
            },
        }
        "vector": [0.0, 0.0, 0.0, 0.0, 0.0], # required - vectorized highlight  
        "transformations": [
            {
                "name": "string",
                "endpoint": "string",
                "version-history": [
                    {
                        "text": "string",
                        "date": "Date"
                    }
                ]
            },
            "question": {
                "endpoint": "string",
                "version-history": [
                    {
                        "text": "string",
                        "date": "Date"
                    }
                ]
            },
            "quiz": {
                "endpoint": "string",
                "version-history": [
                    {
                        "text": "string",
                        "date": "Date"
                    }
                ]
            },
            "image": {
                "endpoint": "string",
                "version-history": [
                    {
                        "text": "string",
                        "date": "Date"
                    }
                ]
            },
            "tags": {
                "endpoint": "string",
                "version-history": [
                    {
                        "text": "string",
                        "date": "Date"
                    }
                ]
            }
        ]
    }
}

add highlight processing:
1. check if highlight is already in db
2. if not, add highlight to db
3. add vectorized highlight to db
4. add specified transformations to db

options for llm:
- transform highlight into a question
- transform highlight into tldr
- transform highlight into Q&A flashcard
- transform highlight into a picture
- transform highlight into a list of tags

POST /highlights/highlight - add highlight to db
{
    "highlight": "string", # required
    "transformations" : [
        "tldr",
        "question",
        "image",
        "tags"
    ] # any endpoint from the /transformations/ endpoint
    "source": {
        "url": "string", # optional
        "book": {
            "title": "string",
            "author": "string",
            "page": "string"
        },
    }
}
'''


@ingest_router.post("/highlight")
async def add_highlight(highlight: Highlight, client: AsyncClient = Depends(get_client)):
    processed_highlight = {
        "highlight": highlight.highlight,
        "meta": {
            "source": highlight.source,
            "transformations": highlight.transformations,
            "margin_notes": highlight.margin_notes or []
        },
        "vector": highlight.vector or [0.0, 0.0, 0.0, 0.0, 0.0],
        "published": highlight.published or False,
    }
    # call each transformation endpoint and await response and add to highlight
    for idx, transformation in enumerate(highlight.transformations):
        # replace name with call to transformation endpoint
        # check if endpoint is valid by calling it
        # if invalid, raise error
        res = await client.post(f"http://127.0.0.1:8000/transform/{transformation}", json={"text": highlight.highlight}, headers={"Content-Type": "application/json"})
        if res.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid transformation")
        
        print(res.json())
    
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

    if highlight.source is not None:
        # check if source_type is valid
        if highlight.source.source_type not in SourceType:
            raise HTTPException(status_code=400, detail="Invalid source type")
        if highlight.source.source_type == SourceType.book:
            if highlight.source.book is None:
                raise HTTPException(
                    status_code=400, detail="Missing book details for book source type")
            try:
                book_data = highlight.source.book.dict()
                print(book_data)
                # 'Source' object does not support item assignment

                # processed_highlight["meta"]["source"]["book"] = book_data
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=400, detail="Invalid book details for book source type")

    return processed_highlight
