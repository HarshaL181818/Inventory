from retail_mas_demo.agents.base import BaseAgent
from retail_mas_demo.llm.ollama_runner import run_ollama

class JDAnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__("JD Analyzer")

    def analyze(self, title: str, description: str) -> str:
        prompt = f"""
You are an expert HR assistant. Analyze the following Job Title and Job Description, and extract the following details in structured JSON format:

- education: with keys 'required_degree' and 'field'
- skills:
    - programming_languages (list)
    - tools_and_technologies (list)
    - soft_skills (list)
- responsibilities (list format)
- experience:
    - years
    - preferred_domains (list)

Job Title: {title}
Job Description: {description}

Return only valid JSON, like:
{{
  "education": {{
    "required_degree": "...",
    "field": "..."
  }},
  "skills": {{
    "programming_languages": ["..."],
    "tools_and_technologies": ["..."],
    "soft_skills": ["..."]
  }},
  "responsibilities": ["..."],
  "experience": {{
    "years": "...",
    "preferred_domains": ["..."]
  }}
}}
        """.strip()

        return run_ollama(prompt)
