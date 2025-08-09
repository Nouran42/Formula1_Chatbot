from fastapi import FastAPI
from pydantic import BaseModel
from langchain_astradb import AstraDBVectorStore
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings
import os
from dotenv import load_dotenv
from rag_retrieval import answer_question 


load_dotenv()

ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_COLLECTION = os.getenv("ASTRA_DB_COLLECTION")

vector_store = AstraDBVectorStore(
    collection_name=ASTRA_DB_COLLECTION,
    embedding=OllamaEmbeddings(model="llama3.2"),
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    token=ASTRA_DB_APPLICATION_TOKEN
)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

llm = ChatOllama(
    model="llama3.2",
    temperature=0.0
)

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(req: QuestionRequest):
    docs = retriever.get_relevant_documents(req.question)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = ChatPromptTemplate.from_template(
        """You are an expert on Formula 1.
        Use the following context to answer the question accurately and concisely.
        
        Context:
        {context}
        
        Question:
        {question}
        
        Answer:"""
    )

    final_prompt = prompt.format(context=context, question=req.question)
    response = llm.invoke(final_prompt)
    return {"answer": response.content}
