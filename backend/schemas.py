# backend/schemas.py

from pydantic import BaseModel
from typing import List, Optional


class VariationRequest(BaseModel):
    """
    A single variation generation request.
    Each variation has:
    - parameters (text rules)
    - an index (optional, for UI)
    """
    parameters: str
    index: Optional[int] = None


class BatchRequest(BaseModel):
    """
    The full request sent from app.py to dispatcher.
    Includes:
    - original base message
    - a list of variation requests
    """
    original_message: str
    variations: List[VariationRequest]


class VariantResult(BaseModel):
    """
    A single Groq result after cleanup:
    {
        "index": 1,
        "variant_message": "..."
    }
    """
    index: int
    variant_message: str


class BatchResult(BaseModel):
    """
    Final aggregated results.
    Sent back to app.py for displaying + exporting.
    """
    results: List[VariantResult]
