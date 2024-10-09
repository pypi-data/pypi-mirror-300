# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["SearchCreateParams"]


class SearchCreateParams(TypedDict, total=False):
    max_matches: float
    """The maximum number of results to return. optional for result_mode exact"""

    query: str
    """Search query."""

    result_mode: Literal["exact", "best"]
    """The mode of the search. Valid values are 'exact' or 'best'."""

    scope: Literal["person", "company"]
    """The scope of the search. Valid values are 'person' or 'company'."""
