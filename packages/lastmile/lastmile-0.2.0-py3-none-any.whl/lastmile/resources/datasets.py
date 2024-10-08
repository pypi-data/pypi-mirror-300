# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ..types import (
    dataset_get_params,
    dataset_create_params,
    dataset_get_view_params,
    dataset_upload_file_params,
    dataset_refine_labels_params,
    dataset_upload_split_files_params,
    dataset_finalize_file_uploads_params,
)
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
from ..types.dataset_get_response import DatasetGetResponse
from ..types.dataset_create_response import DatasetCreateResponse
from ..types.dataset_get_view_response import DatasetGetViewResponse
from ..types.dataset_upload_file_response import DatasetUploadFileResponse
from ..types.dataset_refine_labels_response import DatasetRefineLabelsResponse
from ..types.dataset_upload_split_files_response import DatasetUploadSplitFilesResponse
from ..types.dataset_finalize_file_uploads_response import DatasetFinalizeFileUploadsResponse

__all__ = ["DatasetsResource", "AsyncDatasetsResource"]


class DatasetsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DatasetsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/lastmile-ai/lastmile-python#accessing-raw-response-data-eg-headers
        """
        return DatasetsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DatasetsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/lastmile-ai/lastmile-python#with_streaming_response
        """
        return DatasetsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        description: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DatasetCreateResponse:
        """
        Description of create

        Args:
          description: Human-readable description of the dataset, if one exists.

          name: Human-readable name for the dataset, if one exists.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/2/auto_eval/dataset/create",
            body=maybe_transform(
                {
                    "description": description,
                    "name": name,
                },
                dataset_create_params.DatasetCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetCreateResponse,
        )

    def finalize_file_uploads(
        self,
        *,
        dataset_id: dataset_finalize_file_uploads_params.DatasetID,
        s3_pre_signed_upload_urls: List[str],
        split_labels: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DatasetFinalizeFileUploadsResponse:
        """
        Description of finalize_file_uploads

        Args:
          s3_pre_signed_upload_urls: Upload URLs that have completed and whose uploaded files should be marked as
              ready for use.

          split_labels: The sequence of labels for the dataset splits, parallel to the sequence of URLs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/2/auto_eval/dataset/finalize_file_uploads",
            body=maybe_transform(
                {
                    "dataset_id": dataset_id,
                    "s3_pre_signed_upload_urls": s3_pre_signed_upload_urls,
                    "split_labels": split_labels,
                },
                dataset_finalize_file_uploads_params.DatasetFinalizeFileUploadsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetFinalizeFileUploadsResponse,
        )

    def get(
        self,
        *,
        id: dataset_get_params.ID,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DatasetGetResponse:
        """
        Description of get

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/2/auto_eval/dataset/get",
            body=maybe_transform({"id": id}, dataset_get_params.DatasetGetParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetGetResponse,
        )

    def get_view(
        self,
        *,
        dataset_file_id: dataset_get_view_params.DatasetFileID,
        dataset_id: dataset_get_view_params.DatasetID,
        after: int | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DatasetGetViewResponse:
        """
        Description of get_view

        Args:
          after: Pagination: The index, by row-order, after which to query results.

          limit: Pagination: The maximum number of results to return on this page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/2/auto_eval/dataset/get_view",
            body=maybe_transform(
                {
                    "dataset_file_id": dataset_file_id,
                    "dataset_id": dataset_id,
                    "after": after,
                    "limit": limit,
                },
                dataset_get_view_params.DatasetGetViewParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetGetViewResponse,
        )

    def refine_labels(
        self,
        *,
        dataset_id: dataset_refine_labels_params.DatasetID,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DatasetRefineLabelsResponse:
        """
        Description of refine_labels

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/2/auto_eval/dataset/refine_labels",
            body=maybe_transform({"dataset_id": dataset_id}, dataset_refine_labels_params.DatasetRefineLabelsParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetRefineLabelsResponse,
        )

    def upload_file(
        self,
        *,
        dataset_id: dataset_upload_file_params.DatasetID,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DatasetUploadFileResponse:
        """
        Description of upload_file

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/2/auto_eval/dataset/upload_file",
            body=maybe_transform({"dataset_id": dataset_id}, dataset_upload_file_params.DatasetUploadFileParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetUploadFileResponse,
        )

    def upload_split_files(
        self,
        *,
        dataset_id: dataset_upload_split_files_params.DatasetID,
        split_labels: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DatasetUploadSplitFilesResponse:
        """
        Description of upload_split_files

        Args:
          split_labels: A sequence of labels for the dataset splits, for which we will generate a
              parallel list of upload destination URLs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/2/auto_eval/dataset/upload_split_files",
            body=maybe_transform(
                {
                    "dataset_id": dataset_id,
                    "split_labels": split_labels,
                },
                dataset_upload_split_files_params.DatasetUploadSplitFilesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetUploadSplitFilesResponse,
        )


class AsyncDatasetsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDatasetsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/lastmile-ai/lastmile-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDatasetsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDatasetsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/lastmile-ai/lastmile-python#with_streaming_response
        """
        return AsyncDatasetsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        description: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DatasetCreateResponse:
        """
        Description of create

        Args:
          description: Human-readable description of the dataset, if one exists.

          name: Human-readable name for the dataset, if one exists.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/2/auto_eval/dataset/create",
            body=await async_maybe_transform(
                {
                    "description": description,
                    "name": name,
                },
                dataset_create_params.DatasetCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetCreateResponse,
        )

    async def finalize_file_uploads(
        self,
        *,
        dataset_id: dataset_finalize_file_uploads_params.DatasetID,
        s3_pre_signed_upload_urls: List[str],
        split_labels: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DatasetFinalizeFileUploadsResponse:
        """
        Description of finalize_file_uploads

        Args:
          s3_pre_signed_upload_urls: Upload URLs that have completed and whose uploaded files should be marked as
              ready for use.

          split_labels: The sequence of labels for the dataset splits, parallel to the sequence of URLs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/2/auto_eval/dataset/finalize_file_uploads",
            body=await async_maybe_transform(
                {
                    "dataset_id": dataset_id,
                    "s3_pre_signed_upload_urls": s3_pre_signed_upload_urls,
                    "split_labels": split_labels,
                },
                dataset_finalize_file_uploads_params.DatasetFinalizeFileUploadsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetFinalizeFileUploadsResponse,
        )

    async def get(
        self,
        *,
        id: dataset_get_params.ID,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DatasetGetResponse:
        """
        Description of get

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/2/auto_eval/dataset/get",
            body=await async_maybe_transform({"id": id}, dataset_get_params.DatasetGetParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetGetResponse,
        )

    async def get_view(
        self,
        *,
        dataset_file_id: dataset_get_view_params.DatasetFileID,
        dataset_id: dataset_get_view_params.DatasetID,
        after: int | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DatasetGetViewResponse:
        """
        Description of get_view

        Args:
          after: Pagination: The index, by row-order, after which to query results.

          limit: Pagination: The maximum number of results to return on this page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/2/auto_eval/dataset/get_view",
            body=await async_maybe_transform(
                {
                    "dataset_file_id": dataset_file_id,
                    "dataset_id": dataset_id,
                    "after": after,
                    "limit": limit,
                },
                dataset_get_view_params.DatasetGetViewParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetGetViewResponse,
        )

    async def refine_labels(
        self,
        *,
        dataset_id: dataset_refine_labels_params.DatasetID,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DatasetRefineLabelsResponse:
        """
        Description of refine_labels

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/2/auto_eval/dataset/refine_labels",
            body=await async_maybe_transform(
                {"dataset_id": dataset_id}, dataset_refine_labels_params.DatasetRefineLabelsParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetRefineLabelsResponse,
        )

    async def upload_file(
        self,
        *,
        dataset_id: dataset_upload_file_params.DatasetID,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DatasetUploadFileResponse:
        """
        Description of upload_file

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/2/auto_eval/dataset/upload_file",
            body=await async_maybe_transform(
                {"dataset_id": dataset_id}, dataset_upload_file_params.DatasetUploadFileParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetUploadFileResponse,
        )

    async def upload_split_files(
        self,
        *,
        dataset_id: dataset_upload_split_files_params.DatasetID,
        split_labels: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DatasetUploadSplitFilesResponse:
        """
        Description of upload_split_files

        Args:
          split_labels: A sequence of labels for the dataset splits, for which we will generate a
              parallel list of upload destination URLs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/2/auto_eval/dataset/upload_split_files",
            body=await async_maybe_transform(
                {
                    "dataset_id": dataset_id,
                    "split_labels": split_labels,
                },
                dataset_upload_split_files_params.DatasetUploadSplitFilesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetUploadSplitFilesResponse,
        )


class DatasetsResourceWithRawResponse:
    def __init__(self, datasets: DatasetsResource) -> None:
        self._datasets = datasets

        self.create = to_raw_response_wrapper(
            datasets.create,
        )
        self.finalize_file_uploads = to_raw_response_wrapper(
            datasets.finalize_file_uploads,
        )
        self.get = to_raw_response_wrapper(
            datasets.get,
        )
        self.get_view = to_raw_response_wrapper(
            datasets.get_view,
        )
        self.refine_labels = to_raw_response_wrapper(
            datasets.refine_labels,
        )
        self.upload_file = to_raw_response_wrapper(
            datasets.upload_file,
        )
        self.upload_split_files = to_raw_response_wrapper(
            datasets.upload_split_files,
        )


class AsyncDatasetsResourceWithRawResponse:
    def __init__(self, datasets: AsyncDatasetsResource) -> None:
        self._datasets = datasets

        self.create = async_to_raw_response_wrapper(
            datasets.create,
        )
        self.finalize_file_uploads = async_to_raw_response_wrapper(
            datasets.finalize_file_uploads,
        )
        self.get = async_to_raw_response_wrapper(
            datasets.get,
        )
        self.get_view = async_to_raw_response_wrapper(
            datasets.get_view,
        )
        self.refine_labels = async_to_raw_response_wrapper(
            datasets.refine_labels,
        )
        self.upload_file = async_to_raw_response_wrapper(
            datasets.upload_file,
        )
        self.upload_split_files = async_to_raw_response_wrapper(
            datasets.upload_split_files,
        )


class DatasetsResourceWithStreamingResponse:
    def __init__(self, datasets: DatasetsResource) -> None:
        self._datasets = datasets

        self.create = to_streamed_response_wrapper(
            datasets.create,
        )
        self.finalize_file_uploads = to_streamed_response_wrapper(
            datasets.finalize_file_uploads,
        )
        self.get = to_streamed_response_wrapper(
            datasets.get,
        )
        self.get_view = to_streamed_response_wrapper(
            datasets.get_view,
        )
        self.refine_labels = to_streamed_response_wrapper(
            datasets.refine_labels,
        )
        self.upload_file = to_streamed_response_wrapper(
            datasets.upload_file,
        )
        self.upload_split_files = to_streamed_response_wrapper(
            datasets.upload_split_files,
        )


class AsyncDatasetsResourceWithStreamingResponse:
    def __init__(self, datasets: AsyncDatasetsResource) -> None:
        self._datasets = datasets

        self.create = async_to_streamed_response_wrapper(
            datasets.create,
        )
        self.finalize_file_uploads = async_to_streamed_response_wrapper(
            datasets.finalize_file_uploads,
        )
        self.get = async_to_streamed_response_wrapper(
            datasets.get,
        )
        self.get_view = async_to_streamed_response_wrapper(
            datasets.get_view,
        )
        self.refine_labels = async_to_streamed_response_wrapper(
            datasets.refine_labels,
        )
        self.upload_file = async_to_streamed_response_wrapper(
            datasets.upload_file,
        )
        self.upload_split_files = async_to_streamed_response_wrapper(
            datasets.upload_split_files,
        )
