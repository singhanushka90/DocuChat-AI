from fastapi import Depends,APIRouter,File
from auth.dependencies import get_current_user
from models import ChatRequest
router=APIRouter()
@router.post("/chat")
def chat(
    data: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    print("Current user:", current_user["email"])

    if chatbot is None:
        return {"error": "Please upload a PDF first."}

    response = chatbot.invoke(
        {"input": data.input},
        config={"configurable": {"session_id": data.session_id}}
    )

    return {
        "question": data.input,
        "session": data.session_id,
        "user": current_user["email"],
        "answer": response.get("answer", "No answer found")
    }