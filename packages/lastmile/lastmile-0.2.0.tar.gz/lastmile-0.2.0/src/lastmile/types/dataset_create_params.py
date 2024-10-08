# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["DatasetCreateParams"]


class DatasetCreateParams(TypedDict, total=False):
    description: str
    """Human-readable description of the dataset, if one exists."""

    name: str
    """Human-readable name for the dataset, if one exists."""
