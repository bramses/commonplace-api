from pydantic import BaseModel, Field, ValidationError
from typing import Dict, List, Any
from enum import Enum

class SourceType(str, Enum):
    book = "book"
    article = "article"
    video = "video"

class Book(BaseModel):
    title: str
    author: str
    page: str

class Article(BaseModel):
    title: str
    author: str
    anchor: str

class Video(BaseModel):
    title: str
    timestamp: str

class Idea(BaseModel):
    context: str

class Source(BaseModel):
    url: str
    source_type: SourceType
    book: Book = None 
    article: Article = None
    video: Video = None
    idea: Idea = None

    # def __init__(self, **data: Any):
    #     super().__init__(**data)

    #     if self.source_type == SourceType.book:
    #         if self.book is None:
    #             raise ValueError("Missing book details for book source type")
    #         try:
    #             Book(**self.book)
    #         except ValidationError:
    #             raise ValueError("Invalid book details for book source type")
    #     elif self.source_type == SourceType.article:
    #         if self.article is None:
    #             raise ValueError("Missing article details for article source type")
    #         try:
    #             Article(**self.article)
    #         except ValidationError:
    #             raise ValueError("Invalid article details for article source type")
    #     elif self.source_type == SourceType.video:
    #         if self.video is None:
    #             raise ValueError("Missing video details for video source type")
    #         try:
    #             Video(**self.video)
    #         except ValidationError:
    #             raise ValueError("Invalid video details for video source type")


class Transformations(BaseModel):
    # list of dicts with name, endpoint, version-history
    transformations: List[Dict[str, Any]]

class Highlight(BaseModel):
    highlight: str = Field(...,
                       example="The greatest use of a life is to spend it on something that will outlast it.")
    source: Source = Field(None, example={"url": "https://www.brainyquote.com/quotes/william_james_101063", "source_type": "article", "author": "William James", "title": "William James - The greatest use of a life is to spend it...", "anchor": None})
    transformations: List[str] = Field(None, example=["tldr", "question", "image", "tags"])
    vector: List[float] = Field([0.0, 0.0, 0.0, 0.0, 0.0], example=[0.0, 0.0, 0.0, 0.0, 0.0])
    published: bool = Field(False, example=True)
    id: str = Field(None, example="5f8a9b3b9d9d9d9d9d9d9d9d")
    margin_notes: List[Dict] = Field(None, example=[{ "note": "This is a margin note", "date": "today" }])