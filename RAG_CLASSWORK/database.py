#database.py

import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env file")


# Create embedding model
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=API_KEY
)


# Connect to ChromaDB
vector_store = Chroma(
    collection_name="myCollection",
    embedding_function=embeddings,
    persist_directory="./chromadb"
)


# Store documents
def addData(data: list[str]):
    if not data:
        raise ValueError("No documents provided")

    vector_store.add_texts(texts=data)

    return "Documents stored successfully!"


# Retrieve all stored documents
def getData():
    return vector_store.get()


# Search relevant documents using similarity search
def askQuestion(question: str):
    results = vector_store.similarity_search(
        query=question,
        k=3
    )

    return results
