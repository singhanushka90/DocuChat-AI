from loaders.file_loader import load_uploaded_file
from models import ChatRequest
from fastapi import FastAPI,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
from retrievers.rag_pipeline import setup_rag_pipeline,get_chatbot

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file:UploadFile=File(...)):
    docs=await load_uploaded_file(file)
    result=setup_rag_pipeline(docs)
    return result


@app.post("/chat")
def chat(data:ChatRequest):
    chatbot=get_chatbot()
    if chatbot is None:
        return {"error":"Please Upload File First"}
    response=chatbot.invoke({"input":data.input},config={"configurable":{"session_id":data.session_id}})
    return{
        "question":data.input,
        "session":data.session_id,
        "answer":response.get("answer","No Answer found")
    }