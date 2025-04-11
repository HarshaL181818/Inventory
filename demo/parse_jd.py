import json, re, sqlite3, uuid
from retail_mas_demo.agents.jdAnalyzer import JDAnalyzerAgent
def analyze_and_store(title, description):
    agent = JDAnalyzerAgent()
    raw_response = agent.analyze(title, description)

    print("Raw Response:", raw_response)  # Debugging output to check the raw response

    json_string = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_response, re.DOTALL)
    if json_string:
        cleaned = json_string.group(1)
    else:
        cleaned = re.search(r"(\{.*\})", raw_response, re.DOTALL).group(1)

    jd_data = json.loads(cleaned)
    job_id = str(uuid.uuid4())

    # Extract experience information with fallbacks for missing values
    experience_years = jd_data.get('experience', {}).get('years', 'N/A')  # Default to 'N/A' if missing
    experience_domains = jd_data.get('experience', {}).get('preferred_domains', [])
    experience_domains_str = ', '.join(experience_domains) if experience_domains else 'N/A'

    # If experience_years is null, set it to 'N/A'
    if experience_years is None:
        experience_years = 'N/A'

    conn = sqlite3.connect("jd_analysis.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_descriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id TEXT,
        title TEXT,
        education_degree TEXT,
        education_field TEXT,
        programming_languages TEXT,
        tools_and_technologies TEXT,
        soft_skills TEXT,
        responsibilities TEXT,
        experience_years TEXT,
        experience_domains TEXT
    )
    """)

    cursor.execute("""
    INSERT INTO job_descriptions (
        job_id, title,
        education_degree, education_field,
        programming_languages, tools_and_technologies, soft_skills,
        responsibilities,
        experience_years, experience_domains
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        job_id,
        title,
        jd_data['education']['required_degree'],
        jd_data['education']['field'],
        ', '.join(jd_data['skills']['programming_languages']),
        ', '.join(jd_data['skills']['tools_and_technologies']),
        ', '.join(jd_data['skills']['soft_skills']),
        json.dumps(jd_data['responsibilities']),
        experience_years,
        experience_domains_str
    ))

    conn.commit()
    conn.close()

    jd_data["job_id"] = job_id
    return jd_data
