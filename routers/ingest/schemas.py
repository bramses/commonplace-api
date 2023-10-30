from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from enum import Enum

class SourceType(str, Enum):
    book = "book"
    article = "article"
    video = "video"
    idea = "idea"

class Book(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    page: Optional[str] = None
    url: Optional[str] = None

class Article(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    anchor: Optional[str] = None
    url: Optional[str] = None

class Video(BaseModel):
    title: Optional[str] = None
    timestamp: Optional[str] = None
    url: Optional[str] = None

class Idea(BaseModel):
    context: Optional[str] = None
    url: Optional[str] = None

class Source(BaseModel):
    category: str = None
    book: Optional[Book] = None
    article: Optional[Article] = None
    video: Optional[Video] = None
    idea: Optional[Idea] = None


class Transformations(BaseModel):
    # list of dicts with name, endpoint, version-history
    transformations: List[Dict[str, Any]]

class Highlight(BaseModel):
    highlight: str = Field(...,
                       example="The greatest use of a life is to spend it on something that will outlast it.")
    source: Source = Field(None, example={"article": { "url": "https://www.brainyquote.com/quotes/william_james_101063", "author": "William James", "title": "William James - The greatest use of a life is to spend it...", "anchor": None }})
    transformations: List[str] = Field(None, example=["tldr", "question", "image"])
    vector: Optional[List[float]] = Field(None)
    published: bool = Field(False, example=True)
    id: Optional[str] = Field(None, example="5f8a9b3b9d9d9d9d9d9d9d9d")
    margin_notes: List[str] = Field(None, example=["This is a margin note", "This is another margin note with a url https://www.google.com"])

    class Config:
        json_schema_extra = {
            "example": {
                "highlight": "The greatest use of a life is to spend it on something that will outlast it.",
                "source": {"article": { "url": "https://www.brainyquote.com/quotes/william_james_101063", "author": "William James", "title": "William James - The greatest use of a life is to spend it...", "anchor": None }},
                "transformations": ["tldr", "question", "image"],
                "published": True,
                "id": "5f8a9b3b9d9d9d9d9d9d9d9d",
                "margin_notes": ["This is a margin note", "This is another margin note with a url https://www.google.com"]
            }
        }