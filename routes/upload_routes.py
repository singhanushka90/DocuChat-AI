from fastapi import Depends,APIRouter,File,UploadFile
from auth.dependencies import get_current_user
router=APIRouter()
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):

    # ab yahan tum upload logic chalao
    return {
        "message": "File uploaded successfully",
        "uploaded_by": current_user["email"],
        "filename":file.filename
    }