from typing import Dict, Optional

from pydantic import BaseModel


class ResponseSchema(BaseModel):
    """response schema."""

    message: str
    error: bool
    data: Optional[Dict]
