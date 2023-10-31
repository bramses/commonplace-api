from fastapi import APIRouter, HTTPException, Body
from dependencies import humanize_now
from ai.dependencies import chat_completion
from .schemas import TextModel



router = APIRouter(
    prefix="/transform",
    tags=["transform"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


def get_mock_highlight(id: str):
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


def append_to_version_history(highlight, endpoint, text):
    for transformation in highlight["meta"]["transformations"]:
        if transformation["endpoint"] == endpoint:
            transformation["version_history"].insert(0, {"text": text, "created_at": humanize_now()})
            break
    return highlight

# --> IM EATING <--

async def update_highlight_by_id(id: str, prompt: str, endpoint: str, body: TextModel = Body(...)):
    highlight = get_mock_highlight(id) # get highlight from db eventually
    
    if id is None:
        raise HTTPException(status_code=400, detail="Highlight ID cannot be empty")
    if body.text is None or body.text == "":
        # get text from highlight id to have ai generate a tldr
        text = highlight["highlight"]
        prompt = prompt.format(text)
        # call GPT-4 chat endpoint and await response
        text = await chat_completion(prompt, dry_run=body.dry_run)
    else:
        text = body.text # use text from request body to generate tldr
 
    highlight = append_to_version_history(highlight, endpoint, text)
    
    return highlight