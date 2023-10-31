from typing import Optional
from pydantic import BaseModel

class TextModel(BaseModel):
    text: Optional[str] = None
    dry_run: Optional[bool] = False