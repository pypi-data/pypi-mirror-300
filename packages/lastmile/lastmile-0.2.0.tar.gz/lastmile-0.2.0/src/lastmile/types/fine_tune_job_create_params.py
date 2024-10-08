# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "FineTuneJobCreateParams",
    "FineTuneJobConfig",
    "FineTuneJobConfigBaselineModelID",
    "FineTuneJobConfigDatasetID",
    "FineTuneJobConfigHyperparameters",
    "FineTuneJobConfigHyperparametersParam",
]


class FineTuneJobCreateParams(TypedDict, total=False):
    fine_tune_job_config: Required[Annotated[FineTuneJobConfig, PropertyInfo(alias="fineTuneJobConfig")]]
    """See repos/lastmile/prisma/schema.prisma:AEFineTuneJobConfig"""


class FineTuneJobConfigBaselineModelID(TypedDict, total=False):
    value: Required[str]


class FineTuneJobConfigDatasetID(TypedDict, total=False):
    value: Required[str]


class FineTuneJobConfigHyperparametersParam(TypedDict, total=False):
    key: Required[str]

    value: Required[str]


class FineTuneJobConfigHyperparameters(TypedDict, total=False):
    params: Required[Iterable[FineTuneJobConfigHyperparametersParam]]
    """Key-value pairs of hyperparameters."""


class FineTuneJobConfig(TypedDict, total=False):
    baseline_model_id: Required[Annotated[FineTuneJobConfigBaselineModelID, PropertyInfo(alias="baselineModelId")]]

    dataset_id: Required[Annotated[FineTuneJobConfigDatasetID, PropertyInfo(alias="datasetId")]]

    hyperparameters: Required[FineTuneJobConfigHyperparameters]
    """Key-value pairs of hyperparameters."""

    description: str
    """Optional description for the job."""

    name: str
    """Optional name for the job."""
