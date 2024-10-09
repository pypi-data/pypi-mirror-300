# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["SearchRetrieveResponse", "SearchRetrieveResponseItem", "SearchRetrieveResponseItemCriteriaAndReason"]


class SearchRetrieveResponseItemCriteriaAndReason(BaseModel):
    criteria: Optional[str] = None
    """Match criteria"""

    match: Optional[bool] = None
    """Whether it's a match"""

    reason: Optional[str] = None
    """Reason for the match"""


class SearchRetrieveResponseItem(BaseModel):
    linkedin_url: str

    name: str

    company: Optional[str] = None
    """Returned only for a person."""

    criteria_and_reasons: Optional[List[SearchRetrieveResponseItemCriteriaAndReason]] = None

    domain: Optional[str] = None
    """Returned only for a company."""

    title: Optional[str] = None
    """Returned only for a person."""


SearchRetrieveResponse: TypeAlias = List[SearchRetrieveResponseItem]
