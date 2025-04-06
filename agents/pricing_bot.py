from agents.base import BaseAgent
from llm.ollama_runner import run_ollama

class PricingBotAgent(BaseAgent):
    def __init__(self):
        super().__init__("Pricing Bot")

    def adjust_price(self, product_name: str, current_price: float, competitor_price: float) -> str:
        prompt = f"Suggest a new price for {product_name}.\nCurrent price: ${current_price}\nCompetitor price: ${competitor_price} while keeping the answer very short and concise"
        return run_ollama(prompt)
