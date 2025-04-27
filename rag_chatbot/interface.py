from transformers import AutoTokenizer, AutoModelForMaskedLM
from rag_chatbot.retriever import Retriever
from rag_chatbot.generator import Generator

class Chatbot:
    def __init__(self):
        self.retriever = Retriever()
        
        # Initialize the Generator directly (no need to pass tokenizer)
        self.generator = Generator()
        self.history = []

    def ask(self, query: str) -> str:
        # Retrieve context from retriever
        hits = self.retriever.retrieve(query)
        
        contexts = [f"{h['name']}: {h.get('price', '')}" for h in hits]
        context_str = " ".join(contexts)  # Join contexts into a single string
        
        # Concatenate query and context
        input_text = query + " " + context_str
        
        # Generate answer using the generator
        answer = self.generator.generate(input_text)
        
        # Add to history
        self.history.append({'query': query, 'answer': answer})
        return answer

