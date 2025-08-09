from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_astradb import AstraDBVectorStore
import os
from dotenv import load_dotenv
import json


load_dotenv()

with open("scraped_f1_content.json", "r", encoding="utf-8") as f:
    raw_docs = json.load(f)

from langchain_core.documents import Document

docs = [
    Document(
        page_content=doc["text"],
        metadata={"source": doc["url"]}
    ) for doc in raw_docs
]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
split_docs = text_splitter.split_documents(docs)

print(f"Split into {len(split_docs)} chunks.")

embeddings = OllamaEmbeddings(model="llama3.2")

token=os.getenv("ASTRA_DB_APPLICATION_TOKEN")
api_endpoint=os.getenv("ASTRA_DB_ENDPOINT") 

vectorstore = AstraDBVectorStore(
    embedding=embeddings,
    collection_name="f1_clean_docs",
    token=token,  
    api_endpoint= api_endpoint
)

vectorstore.add_documents(split_docs)

print("F1 documents stored in Astra DB!")
