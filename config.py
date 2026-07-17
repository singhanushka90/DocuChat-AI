import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI=os.getenv("MONGODB_URI")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
PINECONE_INDEX=os.getenv("PINECONE_INDEX")
GROQ_API_KEY=os.getenv("GROQ_PAI_KEY")