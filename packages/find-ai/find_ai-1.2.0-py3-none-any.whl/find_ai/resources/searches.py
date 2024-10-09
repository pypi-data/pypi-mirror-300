# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import search_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.search_create_response import SearchCreateResponse
from ..types.search_retrieve_response import SearchRetrieveResponse

__all__ = ["SearchesResource", "AsyncSearchesResource"]


class SearchesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SearchesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Find-AI/find-ai-python#accessing-raw-response-data-eg-headers
        """
        return SearchesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SearchesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Find-AI/find-ai-python#with_streaming_response
        """
        return SearchesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        max_matches: float | NotGiven = NOT_GIVEN,
        query: str | NotGiven = NOT_GIVEN,
        result_mode: Literal["exact", "best"] | NotGiven = NOT_GIVEN,
        scope: Literal["person", "company"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchCreateResponse:
        """Starts a search.

        Args:
          max_matches: The maximum number of results to return.

        optional for result_mode exact

          query: Search query.

          result_mode: The mode of the search. Valid values are 'exact' or 'best'.

          scope: The scope of the search. Valid values are 'person' or 'company'.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/searches",
            body=maybe_transform(
                {
                    "max_matches": max_matches,
                    "query": query,
                    "result_mode": result_mode,
                    "scope": scope,
                },
                search_create_params.SearchCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SearchCreateResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchRetrieveResponse:
        """
        The endpoint to poll to check the latest results of a search.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/searches/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SearchRetrieveResponse,
        )


class AsyncSearchesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSearchesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Find-AI/find-ai-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSearchesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSearchesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Find-AI/find-ai-python#with_streaming_response
        """
        return AsyncSearchesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        max_matches: float | NotGiven = NOT_GIVEN,
        query: str | NotGiven = NOT_GIVEN,
        result_mode: Literal["exact", "best"] | NotGiven = NOT_GIVEN,
        scope: Literal["person", "company"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchCreateResponse:
        """Starts a search.

        Args:
          max_matches: The maximum number of results to return.

        optional for result_mode exact

          query: Search query.

          result_mode: The mode of the search. Valid values are 'exact' or 'best'.

          scope: The scope of the search. Valid values are 'person' or 'company'.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/searches",
            body=await async_maybe_transform(
                {
                    "max_matches": max_matches,
                    "query": query,
                    "result_mode": result_mode,
                    "scope": scope,
                },
                search_create_params.SearchCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SearchCreateResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchRetrieveResponse:
        """
        The endpoint to poll to check the latest results of a search.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/searches/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SearchRetrieveResponse,
        )


class SearchesResourceWithRawResponse:
    def __init__(self, searches: SearchesResource) -> None:
        self._searches = searches

        self.create = to_raw_response_wrapper(
            searches.create,
        )
        self.retrieve = to_raw_response_wrapper(
            searches.retrieve,
        )


class AsyncSearchesResourceWithRawResponse:
    def __init__(self, searches: AsyncSearchesResource) -> None:
        self._searches = searches

        self.create = async_to_raw_response_wrapper(
            searches.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            searches.retrieve,
        )


class SearchesResourceWithStreamingResponse:
    def __init__(self, searches: SearchesResource) -> None:
        self._searches = searches

        self.create = to_streamed_response_wrapper(
            searches.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            searches.retrieve,
        )


class AsyncSearchesResourceWithStreamingResponse:
    def __init__(self, searches: AsyncSearchesResource) -> None:
        self._searches = searches

        self.create = async_to_streamed_response_wrapper(
            searches.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            searches.retrieve,
        )
