from agents.base import BaseAgent
from llm.ollama_runner import run_ollama

class InventoryOptimizerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Inventory Optimizer")

    def optimize(self, product_name: str, current_stock: int, predicted_demand: int) -> str:
        prompt = f"Optimize inventory for {product_name}.\nCurrent stock: {current_stock}\nPredicted demand: {predicted_demand} while keeping the answer very short and concise"
        return run_ollama(prompt)
