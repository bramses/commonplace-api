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


class Source(BaseModel):
    url: str
    source_type: SourceType
    book: Book = None 
    article: Article = None
    video: Video = None

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

class Quote(BaseModel):
    quote: str = Field(...,
                       example="The best way to predict the future is to invent it.")
    source: Source = Field(None, example={"url": "https://www.brainyquote.com/quotes/alan_kay_385841", "source_type": "article"})
    transformations: list = Field(None, example=["tldr", "question", "image", "tags"])