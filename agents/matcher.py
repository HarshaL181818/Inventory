from retail_mas_demo.llm.ollama_runner import run_ollama
from retail_mas_demo.agents.base import BaseAgent
import re

import json

class MatchingAgent(BaseAgent):
    

    def extract_json(self, text: str) -> str:
        """
        Extracts the first JSON array or object found in a text response.
        """
        try:
            # Match JSON array or object
            match = re.search(r'(\[.*?\]|\{.*?\})', text, re.DOTALL)
            if match:
                return match.group(1)
            else:
                raise ValueError("No JSON found in response.")
        except Exception as e:
            print(f"Error in extract_json: {e}")
            return "[]"

    def __init__(self):
        super().__init__("Matching Agent")

    def match(self, jd_data, candidates):
        print("started matching");
        prompt = f"""
Given this Job Description:

{json.dumps(jd_data, indent=2)}

Match the following candidates:

{json.dumps(candidates, indent=2)}

Return a JSON array of matches with fields:
[
  {{
    "jd_id": "...",
    "candidate_id": "...",
    "score": 0-100
  }}
]
        """
        response = self.act(prompt)
        print("matching done")
        cleaned = self.extract_json(response)
        
        return json.loads(cleaned)
