from agents.base import BaseAgent
from llm.ollama_runner import run_ollama

class CustomerBehaviorAnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Customer Analyzer")

    def analyze(self, feedback: str, sales_data: str) -> str:
        prompt = f"Analyze customer behavior using this feedback:\n{feedback}\nand this sales data:\n{sales_data} while keeping the answer very short and concise"
        return run_ollama(prompt)
