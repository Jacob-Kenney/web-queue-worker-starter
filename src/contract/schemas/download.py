from pydantic import BaseModel


class DownloadRequest(BaseModel):
    key: str


class DownloadResult(BaseModel):
    url: str
    expires_in: int
