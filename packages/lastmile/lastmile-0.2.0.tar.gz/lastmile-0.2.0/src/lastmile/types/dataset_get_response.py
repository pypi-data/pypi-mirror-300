# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["DatasetGetResponse", "Dataset", "DatasetID", "DatasetOwnerUserID"]


class DatasetID(BaseModel):
    value: str


class DatasetOwnerUserID(BaseModel):
    value: str


class Dataset(BaseModel):
    id: DatasetID

    created_at: datetime = FieldInfo(alias="createdAt")

    owner_user_id: DatasetOwnerUserID = FieldInfo(alias="ownerUserId")

    updated_at: datetime = FieldInfo(alias="updatedAt")

    description: Optional[str] = None
    """Human-readable description of the dataset, if one exists."""

    name: Optional[str] = None
    """Human-readable name for the dataset, if one exists."""


class DatasetGetResponse(BaseModel):
    dataset: Dataset
    """
    A Dataset in the most basic sense: metadata and ownership, but nothing tied to
    its data.
    """
