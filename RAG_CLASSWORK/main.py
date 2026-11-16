from fastapi import FastAPI
from pydantic import BaseModel

# Import database functions
from database import addData, getData

# Import response function
from services import findResponse


app = FastAPI(title="RAG Application")


# Model for document input
class DocumentInput(BaseModel):
    documents: list[str]


# Model for question input
class ChatInput(BaseModel):
    prompt: str


# Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to RAG Application!"}


# Store documents in ChromaDB
@app.post("/collection")
def storeData(data: DocumentInput):
    message = addData(data.documents)

    return {"message": message}


# Get stored documents
@app.get("/collection")
def getCollectionData():
    return getData()


# Ask a question
@app.post("/chat")
def getResponse(query: ChatInput):
    response = findResponse(query.prompt)

    return {"response": response}