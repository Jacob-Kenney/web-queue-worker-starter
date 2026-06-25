from pydantic import BaseModel


class UploadRequest(BaseModel):
    filename: str
    content: str


class UploadResult(BaseModel):
    key: str
