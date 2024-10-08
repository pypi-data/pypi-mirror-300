# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from lastmile import Lastmile, AsyncLastmile
from tests.utils import assert_matches_type
from lastmile.types import (
    DatasetGetResponse,
    DatasetCreateResponse,
    DatasetGetViewResponse,
    DatasetUploadFileResponse,
    DatasetRefineLabelsResponse,
    DatasetUploadSplitFilesResponse,
    DatasetFinalizeFileUploadsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDatasets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Lastmile) -> None:
        dataset = client.datasets.create()
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Lastmile) -> None:
        dataset = client.datasets.create(
            description="description",
            name="name",
        )
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Lastmile) -> None:
        response = client.datasets.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Lastmile) -> None:
        with client.datasets.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_finalize_file_uploads(self, client: Lastmile) -> None:
        dataset = client.datasets.finalize_file_uploads(
            dataset_id={"value": "value"},
            s3_pre_signed_upload_urls=["string", "string", "string"],
            split_labels=["string", "string", "string"],
        )
        assert_matches_type(DatasetFinalizeFileUploadsResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_finalize_file_uploads(self, client: Lastmile) -> None:
        response = client.datasets.with_raw_response.finalize_file_uploads(
            dataset_id={"value": "value"},
            s3_pre_signed_upload_urls=["string", "string", "string"],
            split_labels=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetFinalizeFileUploadsResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_finalize_file_uploads(self, client: Lastmile) -> None:
        with client.datasets.with_streaming_response.finalize_file_uploads(
            dataset_id={"value": "value"},
            s3_pre_signed_upload_urls=["string", "string", "string"],
            split_labels=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetFinalizeFileUploadsResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_get(self, client: Lastmile) -> None:
        dataset = client.datasets.get(
            id={"value": "value"},
        )
        assert_matches_type(DatasetGetResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Lastmile) -> None:
        response = client.datasets.with_raw_response.get(
            id={"value": "value"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetGetResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Lastmile) -> None:
        with client.datasets.with_streaming_response.get(
            id={"value": "value"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetGetResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_get_view(self, client: Lastmile) -> None:
        dataset = client.datasets.get_view(
            dataset_file_id={"value": "value"},
            dataset_id={"value": "value"},
        )
        assert_matches_type(DatasetGetViewResponse, dataset, path=["response"])

    @parametrize
    def test_method_get_view_with_all_params(self, client: Lastmile) -> None:
        dataset = client.datasets.get_view(
            dataset_file_id={"value": "value"},
            dataset_id={"value": "value"},
            after=-2147483648,
            limit=-2147483648,
        )
        assert_matches_type(DatasetGetViewResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_get_view(self, client: Lastmile) -> None:
        response = client.datasets.with_raw_response.get_view(
            dataset_file_id={"value": "value"},
            dataset_id={"value": "value"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetGetViewResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_get_view(self, client: Lastmile) -> None:
        with client.datasets.with_streaming_response.get_view(
            dataset_file_id={"value": "value"},
            dataset_id={"value": "value"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetGetViewResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_refine_labels(self, client: Lastmile) -> None:
        dataset = client.datasets.refine_labels(
            dataset_id={"value": "value"},
        )
        assert_matches_type(DatasetRefineLabelsResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_refine_labels(self, client: Lastmile) -> None:
        response = client.datasets.with_raw_response.refine_labels(
            dataset_id={"value": "value"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetRefineLabelsResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_refine_labels(self, client: Lastmile) -> None:
        with client.datasets.with_streaming_response.refine_labels(
            dataset_id={"value": "value"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetRefineLabelsResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_upload_file(self, client: Lastmile) -> None:
        dataset = client.datasets.upload_file(
            dataset_id={"value": "value"},
        )
        assert_matches_type(DatasetUploadFileResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_upload_file(self, client: Lastmile) -> None:
        response = client.datasets.with_raw_response.upload_file(
            dataset_id={"value": "value"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetUploadFileResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_upload_file(self, client: Lastmile) -> None:
        with client.datasets.with_streaming_response.upload_file(
            dataset_id={"value": "value"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetUploadFileResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_upload_split_files(self, client: Lastmile) -> None:
        dataset = client.datasets.upload_split_files(
            dataset_id={"value": "value"},
            split_labels=["string", "string", "string"],
        )
        assert_matches_type(DatasetUploadSplitFilesResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_upload_split_files(self, client: Lastmile) -> None:
        response = client.datasets.with_raw_response.upload_split_files(
            dataset_id={"value": "value"},
            split_labels=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetUploadSplitFilesResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_upload_split_files(self, client: Lastmile) -> None:
        with client.datasets.with_streaming_response.upload_split_files(
            dataset_id={"value": "value"},
            split_labels=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetUploadSplitFilesResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDatasets:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.create()
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.create(
            description="description",
            name="name",
        )
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncLastmile) -> None:
        response = await async_client.datasets.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncLastmile) -> None:
        async with async_client.datasets.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_finalize_file_uploads(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.finalize_file_uploads(
            dataset_id={"value": "value"},
            s3_pre_signed_upload_urls=["string", "string", "string"],
            split_labels=["string", "string", "string"],
        )
        assert_matches_type(DatasetFinalizeFileUploadsResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_finalize_file_uploads(self, async_client: AsyncLastmile) -> None:
        response = await async_client.datasets.with_raw_response.finalize_file_uploads(
            dataset_id={"value": "value"},
            s3_pre_signed_upload_urls=["string", "string", "string"],
            split_labels=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetFinalizeFileUploadsResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_finalize_file_uploads(self, async_client: AsyncLastmile) -> None:
        async with async_client.datasets.with_streaming_response.finalize_file_uploads(
            dataset_id={"value": "value"},
            s3_pre_signed_upload_urls=["string", "string", "string"],
            split_labels=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetFinalizeFileUploadsResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_get(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.get(
            id={"value": "value"},
        )
        assert_matches_type(DatasetGetResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncLastmile) -> None:
        response = await async_client.datasets.with_raw_response.get(
            id={"value": "value"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetGetResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncLastmile) -> None:
        async with async_client.datasets.with_streaming_response.get(
            id={"value": "value"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetGetResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_get_view(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.get_view(
            dataset_file_id={"value": "value"},
            dataset_id={"value": "value"},
        )
        assert_matches_type(DatasetGetViewResponse, dataset, path=["response"])

    @parametrize
    async def test_method_get_view_with_all_params(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.get_view(
            dataset_file_id={"value": "value"},
            dataset_id={"value": "value"},
            after=-2147483648,
            limit=-2147483648,
        )
        assert_matches_type(DatasetGetViewResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_get_view(self, async_client: AsyncLastmile) -> None:
        response = await async_client.datasets.with_raw_response.get_view(
            dataset_file_id={"value": "value"},
            dataset_id={"value": "value"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetGetViewResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_get_view(self, async_client: AsyncLastmile) -> None:
        async with async_client.datasets.with_streaming_response.get_view(
            dataset_file_id={"value": "value"},
            dataset_id={"value": "value"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetGetViewResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_refine_labels(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.refine_labels(
            dataset_id={"value": "value"},
        )
        assert_matches_type(DatasetRefineLabelsResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_refine_labels(self, async_client: AsyncLastmile) -> None:
        response = await async_client.datasets.with_raw_response.refine_labels(
            dataset_id={"value": "value"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetRefineLabelsResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_refine_labels(self, async_client: AsyncLastmile) -> None:
        async with async_client.datasets.with_streaming_response.refine_labels(
            dataset_id={"value": "value"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetRefineLabelsResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_upload_file(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.upload_file(
            dataset_id={"value": "value"},
        )
        assert_matches_type(DatasetUploadFileResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_upload_file(self, async_client: AsyncLastmile) -> None:
        response = await async_client.datasets.with_raw_response.upload_file(
            dataset_id={"value": "value"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetUploadFileResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_upload_file(self, async_client: AsyncLastmile) -> None:
        async with async_client.datasets.with_streaming_response.upload_file(
            dataset_id={"value": "value"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetUploadFileResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_upload_split_files(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.upload_split_files(
            dataset_id={"value": "value"},
            split_labels=["string", "string", "string"],
        )
        assert_matches_type(DatasetUploadSplitFilesResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_upload_split_files(self, async_client: AsyncLastmile) -> None:
        response = await async_client.datasets.with_raw_response.upload_split_files(
            dataset_id={"value": "value"},
            split_labels=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetUploadSplitFilesResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_upload_split_files(self, async_client: AsyncLastmile) -> None:
        async with async_client.datasets.with_streaming_response.upload_split_files(
            dataset_id={"value": "value"},
            split_labels=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetUploadSplitFilesResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True
