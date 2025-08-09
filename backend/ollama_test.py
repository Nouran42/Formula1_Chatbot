from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.2")

response = llm.invoke("Who won the last Formula 1 race?")
print(response)
