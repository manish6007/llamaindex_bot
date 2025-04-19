from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from services.aws.s3_service import S3Service
import io

router = APIRouter()

@router.get("/download")
def download_file(s3_path: str = Query(..., description="S3 file path")):
    s3_service = S3Service()
    try:
        content = s3_service.download_file(s3_path)
        return StreamingResponse(io.BytesIO(content), media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")
