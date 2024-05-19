from pydantic import BaseModel
from typing import Optional


class Doc(BaseModel):
    Text: Optional[str] = None
