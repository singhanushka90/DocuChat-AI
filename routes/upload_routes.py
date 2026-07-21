from fastapi import Depends,APIRouter,File,UploadFile
from services.rag_pipeline import setup_rag_pipeline
from services.file_loader import load_uploaded_file


from auth.dependencies import get_current_user
router=APIRouter()
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    docs=await load_uploaded_file(file)
    result=setup_rag_pipeline(docs,current_user["_id"])
    result["uploaded_by"]=current_user["email"]
    result["filename"]=file.filename
    return result   