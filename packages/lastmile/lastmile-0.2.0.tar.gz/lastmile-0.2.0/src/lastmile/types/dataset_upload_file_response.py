# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["DatasetUploadFileResponse"]


class DatasetUploadFileResponse(BaseModel):
    s3_pre_signed_upload_url: str = FieldInfo(alias="s3PreSignedUploadUrl")
