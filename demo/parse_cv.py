import json
import sqlite3
import uuid
import re
from retail_mas_demo.agents.cvParser import CVParserAgent

def parse_and_store_cv(cv_text):
    try:
        # Create agent and parse the CV
        agent = CVParserAgent()
        raw_response = agent.parse_cv(cv_text)
        print("Raw Response:", raw_response)  # Debugging output to check the raw response

        # Extract JSON from raw response
        json_string = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_response, re.DOTALL)
        if json_string:
            cleaned = json_string.group(1)
        else:
            cleaned = re.search(r"(\{.*\})", raw_response, re.DOTALL).group(1)

        # Load cleaned JSON data
        cv_data = json.loads(cleaned)
        candidate_id = str(uuid.uuid4())

        # Normalize education fields
        education_data = cv_data.get('education', {})
        education_degree = ', '.join(education_data.get('degree', [])) if isinstance(education_data.get('degree'), list) else education_data.get('degree', 'N/A')
        education_university = ', '.join(education_data.get('university', [])) if isinstance(education_data.get('university'), list) else education_data.get('university', 'N/A')
        education_year = ', '.join(education_data.get('year', [])) if isinstance(education_data.get('year'), list) else education_data.get('year', 'N/A')

        # Open database connection
        conn = sqlite3.connect("jd_analysis.db")
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id TEXT,
            name TEXT,
            email TEXT,
            skills TEXT,
            work_experience TEXT,
            education_degree TEXT,
            education_university TEXT,
            education_year TEXT,
            certifications TEXT,
            achievements TEXT
        )
        """)

        # Insert parsed CV data into the database
        cursor.execute("""
        INSERT INTO candidates (
            candidate_id, name, email, skills, work_experience,
            education_degree, education_university, education_year,
            certifications, achievements
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            candidate_id,
            cv_data.get('name', 'N/A'),
            cv_data.get('email', 'N/A'),
            ', '.join(cv_data.get('skills', [])),
            json.dumps(cv_data.get('work_experience', [])),
            education_degree,
            education_university,
            education_year,
            json.dumps(cv_data.get('certifications', [])),
            json.dumps(cv_data.get('achievements', []))
        ))

        # Commit and close connection
        conn.commit()
        conn.close()

        # Return the stored data with candidate_id
        cv_data["candidate_id"] = candidate_id
        return cv_data

    except Exception as e:
        print(f"Error while parsing and storing CV: {e}")
        return {"error": str(e)}
