from langchain_astradb import AstraDBVectorStore
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_COLLECTION = os.getenv("ASTRA_DB_COLLECTION")  


embeddings = OllamaEmbeddings(model="llama3.2")

vector_store = AstraDBVectorStore(
    collection_name=ASTRA_DB_COLLECTION,
    embedding=embeddings, 
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    token=ASTRA_DB_APPLICATION_TOKEN
)

retriever = vector_store.as_retriever(search_kwargs={"k": 3})  


llm = ChatOllama(
    model="llama3.2",  
    temperature=0.0
)

def answer_question(query):
    docs = retriever.get_relevant_documents(query)

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

    final_prompt = prompt.format(context=context, question=query)

  
    response = llm.invoke(final_prompt)
    return response.content

if __name__ == "__main__":
    while True:
        user_q = input("\nAsk your F1 question (or type 'exit'): ")
        if user_q.lower() == "exit":
            break
        answer = answer_question(user_q)
        print(f"\n {answer}")
