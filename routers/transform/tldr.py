from .dependencies import router as transform_router
from dependencies import humanize_now
from fastapi import Body, HTTPException
from pydantic import BaseModel
from ai.dependencies import chat_completion

class TextModel(BaseModel):
    text: str


@transform_router.post("/tldr")
async def transform_question(body: TextModel = Body(...)):
    text = body.text
    prompt = "tldr to one or two sentences this: " + text
    # call GPT-4 chat endpoint and await response
    text = await chat_completion(prompt)

    print(text)
    return {
        "text": text,
        "created_at": humanize_now() 
    }

def mock_get_text_from_highlight_id(id: str):
    return {
  "highlight": "The greatest use of a life is to spend it on something that will outlast it.",
  "meta": {
    "source": {
      "category": "article",
      "book": None,
      "article": {
        "title": "William James - The greatest use of a life is to spend it...",
        "author": "William James",
        "anchor": None,
        "url": "https://www.brainyquote.com/quotes/william_james_101063"
      },
      "video": None,
      "idea": None
    },
    "transformations": [
      {
        "endpoint": "/transform/tldr",
        "version_history": [
          {
            "text": "~ $4.05e-05 USD",
            "created_at": "2023-10-30 23:28:58"
          }
        ],
        "name": "tldr"
      },
      {
        "endpoint": "/transform/question",
        "version_history": [
          {
            "text": "~ $0.000171 USD",
            "created_at": "2023-10-30 23:28:58"
          }
        ],
        "name": "question"
      }
    ],
    "margin_notes": [
      {
        "text": "This is a margin note",
        "created_at": "2023-10-30 23:28:58"
      },
      {
        "text": "This is another margin note with a url https://www.google.com",
        "created_at": "2023-10-30 23:28:58"
      }
    ]
  },
  "vector": [
    0.011394117,
    -0.0025901592,
    0.012427597,
  ],
  "published": True,
  "created_at": "2023-10-30 23:28:58",
  "updated_at": "2023-10-30 23:28:58",
  "id": "b849493b-dde9-4083-997c-e92b9a8e67ac"
}


@transform_router.post("/tldr/{id}")
async def transform_question_by_highlight_id(id: str, body: TextModel = Body(...)):
    highlight = mock_get_text_from_highlight_id(id)
    if id is None:
        raise HTTPException(status_code=400, detail="Highlight ID cannot be empty")
    if body.text is None:
        # get text from highlight id
        text = highlight.highlight
    else:
        text = body.text
    prompt = "tldr to one or two sentences this: " + text
    # call GPT-4 chat endpoint and await response
    # text = await chat_completion(prompt)

    print(humanize_now())
    # append to where highlight.transformations.endpoint == "tldr".version_history
    # find the tldr endpoint and append new version to version_history to arr 0 idx
    for transformation in highlight["meta"]["transformations"]:
        if transformation["endpoint"] == "/transform/tldr":
            transformation["version_history"].insert(0, {"text": text, "created_at": humanize_now()})
            break
    
   
    
    return highlight