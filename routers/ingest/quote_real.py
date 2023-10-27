from fastapi import APIRouter, Depends, HTTPException
from .schemas import Quote, SourceType

from dependencies import get_token_header

router = APIRouter(
    prefix="/quotes",
    tags=["quotes"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


'''
add quote to db
quote schema example:
{
    "quote": "string", # required
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
        "vector": [0.0, 0.0, 0.0, 0.0, 0.0], # required - vectorized quote  
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

add quote processing:
1. check if quote is already in db
2. if not, add quote to db
3. add vectorized quote to db
4. add specified transformations to db

options for llm:
- transform quote into a question
- transform quote into tldr
- transform quote into Q&A flashcard
- transform quote into a picture
- transform quote into a list of tags

POST /quotes/quote - add quote to db
{
    "quote": "string", # required
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


@router.post("/quote")
async def add_quote(quote: Quote):
    processed_quote = {
        "quote": quote.quote,
        "meta": {
            "source": quote.source,
            "transformations": quote.transformations
        }
    }
    # call each transformation endpoint and await response and add to quote
    for idx, transformation in enumerate(quote.transformations):
        # replace name with call to transformation endpoint
        quote.transformations[idx] = {
            "endpoint": f"/transformations/{transformation}",
            "version-history": [
                {
                    "text": "string",
                    "date": "Date"
                }
            ],
            "name": f"{transformation}"
        }

    if quote.source is not None:
        
        # check if source_type is valid
        if quote.source.source_type not in SourceType:
            raise HTTPException(status_code=400, detail="Invalid source type")
        if quote.source.source_type == SourceType.book:
            if quote.source.book is None:
                raise HTTPException(status_code=400, detail="Missing book details for book source type")
            try:
                book_data = quote.source.book.dict()
                print(book_data)
                # 'Source' object does not support item assignment

                # processed_quote["meta"]["source"]["book"] = book_data 
            except Exception as e:
                print(e)
                raise HTTPException(status_code=400, detail="Invalid book details for book source type")
        



    return processed_quote
