from agents.base import BaseAgent
from llm.ollama_runner import run_ollama

class SupplierNegotiatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Supplier Negotiator")

    def negotiate(self, product_name: str, quantity: int, supplier_terms: str) -> str:
        prompt = f"Negotiate better terms for {product_name}.\nOrder quantity: {quantity}\nCurrent supplier terms: {supplier_terms} while keeping the answer very short and concise"
        return run_ollama(prompt)
