# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "DatasetGetViewResponse",
    "DatasetFileID",
    "DatasetID",
    "DatasetView",
    "DatasetViewData",
    "DatasetViewDataID",
]


class DatasetFileID(BaseModel):
    value: str


class DatasetID(BaseModel):
    value: str


class DatasetViewDataID(BaseModel):
    value: str


class DatasetViewData(BaseModel):
    id: DatasetViewDataID

    row_values: List[Dict[str, object]] = FieldInfo(alias="rowValues")
    """
    Ordered row values with length always equal to `num_rows` on the corresponding
    view.
    """


class DatasetView(BaseModel):
    data: List[DatasetViewData]

    num_cols: int = FieldInfo(alias="numCols")

    num_rows: int = FieldInfo(alias="numRows")


class DatasetGetViewResponse(BaseModel):
    dataset_file_id: DatasetFileID = FieldInfo(alias="datasetFileId")

    dataset_id: DatasetID = FieldInfo(alias="datasetId")

    dataset_view: List[DatasetView] = FieldInfo(alias="datasetView")
