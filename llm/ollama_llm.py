from langchain.llms import Ollama

# You can parameterize this if needed
OLLAMA_MODEL = "llama3.1:8b"
 
def get_llm(model):
    """Returns an Ollama LLM instance ."""
    return Ollama(model=model)
