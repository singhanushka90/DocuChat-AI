# 📄 DocuChat-AI

An AI-powered PDF Chat application built using FastAPI, LangChain, Hugging Face Embeddings, Pinecone, Groq LLM, and MongoDB.

The application allows users to upload PDF documents and ask questions based on the uploaded content using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- User Authentication (JWT)
- Secure PDF Upload
- Text Extraction from PDFs
- Chunking & Embedding Generation
- Pinecone Vector Database Integration
- Retrieval-Augmented Generation (RAG)
- Groq LLM for Question Answering
- MongoDB Integration
- FastAPI Backend
- REST APIs
- Environment Variable Support

---

## 🛠 Tech Stack

### Backend
- FastAPI
- Python
- LangChain
- HuggingFace Embeddings
- Pinecone
- MongoDB
- JWT Authentication
- Groq API

### AI Components
- RAG Pipeline
- Vector Search
- Semantic Search
- Embedding Generation

---

## 📂 Project Structure

```
pdf_chat_ai/
│
├── auth/
├── database/
├── routes/
├── services/
├── uploads/
├── main.py
├── config.py
├── models.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/pdf_chat_ai.git
```

Go inside the folder

```bash
cd pdf_chat_ai
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

Windows

```bash
venv\Scripts\activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your credentials.

Run the server

```bash
uvicorn main:app --reload
```

---

## 🔑 Environment Variables

Create a `.env` file with:

```
MONGODB_URI=
PINECONE_API_KEY=
PINECONE_INDEX=
GROQ_API_KEY=
JWT_SECRET_KEY=
JWT_ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
```

---

## 📌 Current Status

✅ Backend Completed

✅ Authentication

✅ PDF Upload

✅ Pinecone Integration

✅ MongoDB Integration

✅ RAG Pipeline

🚧 Frontend is currently under development.

---

## 📈 Future Improvements

- React Frontend
- Chat History
- Multiple PDF Support
- Conversation Memory
- Source Citations
- Streaming Responses
- Docker Deployment
- AWS Deployment

---

## 👩‍💻 Author

Anushka Singh

AI & Data Science Student
