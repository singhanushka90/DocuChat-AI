import os
import tempfile
from fastapi import UploadFile 
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader

async def load_uploaded_file(file:UploadFile):
    temp=tempfile.NamedTemporaryFile(delete=False,suffix=os.path.splitext(file.filename)[1])
    temp.write(await file.read())
    temp.close()

    if file.filename.endswith(".pdf"):
        loader=PyPDFLoader(temp.name)
    
    elif file.filename.endswith(".txt"):
        loader=TextLoader(temp.name)
    
    elif file.filename.endswith(".docx"):
        loader=Docx2txtLoader(temp.name)
    
    else:
        raise ValueError("Unsupported file type")
    docs=loader.load()
    return docs