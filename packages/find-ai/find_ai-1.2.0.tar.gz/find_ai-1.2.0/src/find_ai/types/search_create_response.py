# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.



from .._models import BaseModel

__all__ = ["SearchCreateResponse", "Poll"]


class Poll(BaseModel):
    token: str

    path: str


class SearchCreateResponse(BaseModel):
    poll: Poll
