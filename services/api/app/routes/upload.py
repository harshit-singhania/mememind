from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.supabase_client import SupabaseClient
import uuid

router = APIRouter()
supabase = SupabaseClient()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        file_ext = file.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_ext}"
        
        public_url = supabase.upload_media(content, file_name=file_name)
        
        if not public_url:
             raise HTTPException(status_code=500, detail="Failed to upload file")
             
        return {"url": public_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
