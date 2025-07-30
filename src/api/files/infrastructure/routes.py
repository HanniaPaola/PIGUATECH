from fastapi import APIRouter, HTTPException, Body, UploadFile, File
from pydantic import BaseModel
import boto3
from botocore.exceptions import ClientError

router = APIRouter(prefix="/api/files", tags=["files"])

BUCKET_NAME = 'informespiguatech'
s3_client = boto3.client('s3')


class FileRequest(BaseModel):
    filename: str


# Nuevo endpoint para subir archivos directamente
@router.post("/upload", response_model=dict)
async def upload_file(file: UploadFile = File(...)):
    try:
        s3_client.upload_fileobj(
            file.file,
            BUCKET_NAME,
            file.filename,
            ExtraArgs={"ContentType": file.content_type}
        )
        return {"filename": file.filename, "message": "Archivo subido exitosamente"}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-presigned-url", response_model=dict)
def generate_presigned_url(data: FileRequest):
    url = s3_client.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': BUCKET_NAME,
            'Key': data.filename,
            'ContentType': 'application/pdf',
        },
        ExpiresIn=3600
    )
    return {"url": url}


@router.get("/get-presigned-url/", response_model=dict)
def get_presigned_url(filename: str):
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': filename},
            ExpiresIn=3600
        )
        return {"url": url}
    except ClientError as e:
        raise HTTPException(status_code=404, detail=str(e))
