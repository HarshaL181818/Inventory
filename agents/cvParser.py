from retail_mas_demo.llm.ollama_runner import run_ollama
from retail_mas_demo.agents.base import BaseAgent

class CVParserAgent(BaseAgent):
    def __init__(self):
        super().__init__("CV Parser")

    def parse_cv(self, cv_text: str) -> str:
        prompt = f"""
You are an expert HR assistant. Parse the following CV text and extract the following details in structured JSON format:

- name
- email
- skills
- work_experience (company, role, duration, responsibilities)
- education (degree, university, year)
- certifications
- achievements

CV Text: {cv_text}

Return only valid JSON, like:
{{
  "name": "...",
  "email": "...",
  "skills": ["..."],
  "work_experience": [
    {{
      "company": "...",
      "role": "...",
      "duration": "...",
      "responsibilities": ["..."]
    }}
  ],
  "education": {{
    "degree": "...",
    "university": "...",
    "year": "..."
  }},
  "certifications": ["..."],
  "achievements": ["..."]
}}
        """.strip()

        return run_ollama(prompt)
