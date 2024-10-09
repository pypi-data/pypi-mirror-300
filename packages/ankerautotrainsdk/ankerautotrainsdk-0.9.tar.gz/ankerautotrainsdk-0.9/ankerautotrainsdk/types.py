from pydantic import BaseModel

class UploadImageResponse(BaseModel):
    url: str
    bucket: str
    storage_id: str
    object_name: str