import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI=os.getenv("MONGODB_URI")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
PINECONE_INDEX=os.getenv("PINECONE_INDEX")
GROQ_API_KEY=os.getenv("GROQ_PAI_KEY")


SECRET_KEY=os.getenv("SECRET_KEY")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",1440))