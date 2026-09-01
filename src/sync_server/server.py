from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class UploadRequest(BaseModel):
    relative_path: str
    size: int
    sha256: str


@app.get("/")
def root():
    return {"message": "Data Sync Server"}


@app.post("/uploads")
def create_upload(request: UploadRequest):

    return {
        "upload_id": "test-upload-id"
    }