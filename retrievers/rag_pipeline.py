import os
from config import MONGODB_URI , PINECONE_API_KEY,GROQ_API_KEY, PINECONE_INDEX
from pinecone import Pinecone

from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_classic.chains.history_aware_retriever import create_history_aware_retriever
from langchain_classic.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_core.stores import InMemoryStore

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

llm = ChatGroq(model_name="llama-3.1-8b-instant")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index(os.getenv("PINECONE_INDEX"))

vectorstore = PineconeVectorStore(
    index=index,
    embedding=embedding
)

docstore = InMemoryStore()

parent_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200
)

child_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

parent_retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=docstore,
    parent_splitter=parent_splitter,
    child_splitter=child_splitter
)

chatbot = None

def get_session(session_id:str):
    return MongoDBChatMessageHistory(connection_string=os.getenv("MONGODB_URI"),
    session_id=session_id,
    database_name="ai_research",
    collection_name="chat_history")


def setup_rag_pipeline(docs):

    global chatbot
    parent_retriever.add_documents(docs)

    print("Parent Retriever Ready")


    parent_docs = parent_splitter.split_documents(docs)
    print(len(parent_docs))
    if not parent_docs:
        return {"error":"Document is empty"}

    bm25 = BM25Retriever.from_documents(parent_docs)
    bm25.k = 4

    print("BM25 Ready")

    hybrid = EnsembleRetriever(
        retrievers=[parent_retriever, bm25],
        weights=[0.6, 0.4]
    )

    print("Hybrid Ready")
    multi = MultiQueryRetriever.from_llm(
        retriever=hybrid,
        llm=llm
    )

    print("Multi Query Ready")
    history_prompt = ChatPromptTemplate.from_messages([

        (
           ("system","""
Given the previous conversation and the latest user question,
rewrite the latest question into a standalone question.

If the latest question refers to something like
'it', 'they', 'this', 'that', 'he', 'she', etc.,
replace it using the conversation history.

Do NOT answer the question.
Only return the rewritten question.
""")
        ),

        MessagesPlaceholder("chat_history"),

        (
            "human",
            "{input}"
        )

    ])

    history_aware = create_history_aware_retriever(llm,multi,history_prompt)

    print("History Aware Ready")

    

    prompt = ChatPromptTemplate.from_messages([

        (
            "system",

            """You are an AI Assistant specialized in answering questions from uploaded documents.
            Instructions:
            1. Answer ONLY from the provided context.
            2. If the answer is not available in the context, reply "I don'y know based on the uploaded documents".
            3. Do not make up facts and hallucinate.
            4. Keep the answer accurate, clear, and well-structured.
            5. If appropriate, explain complex concepts in simple language.
            6. Use bullet points whenever they improve readbility.
            7. If the user asked for the summurary, provide a concise summary.
            8. Manintain continuity using the conversation history
Context:
{context}
"""
        ),

        MessagesPlaceholder("chat_history"),

        (
            "human",
            "{input}"
        )

    ])


    document_chain = create_stuff_documents_chain(

        llm,

        prommpt)

    rag_chain = create_retrieval_chain(

        history_aware,

        document_chain)

    chatbot = RunnableWithMessageHistory(

        rag_chain,

        get_session,

        input_messages_key="input",

        history_messages_key="chat_history",
        output_messages_key="answer"

    )

    print("Chatbot Ready")
    return {"message": "File Uploaded Successfully","pages": len(docs)}

    
def get_chatbot():
    return chatbot







