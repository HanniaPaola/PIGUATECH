from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3

app = FastAPI()

# CORS para que frontend pueda llamar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción pon tu dominio aquí
    allow_methods=["*"],
    allow_headers=["*"],
)

s3_client = boto3.client('s3')

BUCKET_NAME = 'informespiguatech'

class FileRequest(BaseModel):
    filename: str

@app.post("/generate-presigned-url")
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
@app.get("/get-presigned-url/")
def get_presigned_url(filename: str):
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': filename},
            ExpiresIn=3600  # 1 hora
        )
        return {"url": url}
    except ClientError as e:
        raise HTTPException(status_code=404, detail=str(e))
