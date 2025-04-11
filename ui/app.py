from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Import CORS
import sqlite3
import pandas as pd
import os
import json

from retail_mas_demo.demo.parse_cv import parse_and_store_cv
from retail_mas_demo.demo.parse_jd import analyze_and_store

app = Flask(__name__, static_folder='public')

# Enable CORS for all routes (adjust based on your requirements)
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def analyze_jd():
    """
    Route to handle analyzing the job description.
    """
    data = request.json
    title = data.get('title', '')
    description = data.get('description', '')

    try:
        result = analyze_and_store(title, description)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    """
    Serve static files (React build)
    """
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
    
@app.route('/api/get_all_jds', methods=['GET'])
def get_all_jds():
    """
    Route to fetch all job descriptions from the database.
    """
    try:
        conn = sqlite3.connect("jd_analysis.db")
        # Fetch table as DataFrame
        df = pd.read_sql_query("SELECT * FROM job_descriptions", conn)

        # Convert DataFrame to list of dictionaries
        job_descriptions = df.to_dict(orient='records')

        print(job_descriptions)  # Log the fetched data for debugging

        conn.close()
        return jsonify(job_descriptions), 200
    except Exception as e:
        print(f"Error fetching job descriptions: {e}")  # Log the error for debugging
        return jsonify({"error": str(e)}), 500


@app.route('/api/upload_cv', methods=['POST'])
def upload_cv():
    """
    Route to handle uploading a CV (PDF), parse it, and store in the database.
    """
    try:
        # Get the uploaded CV file
        cv_file = request.files['cv']
        cv_text = extract_text_from_pdf(cv_file)  # Function to extract raw text from PDF
        
        # Parse CV and store in the database
        parsed_cv_data = parse_and_store_cv(cv_text)
        return jsonify(parsed_cv_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/save_weights_and_timeslots', methods=['POST'])
def save_weights_and_timeslots():
    """
    Route to save weights and interview time slots for a selected JD.
    """
    try:
        data = request.get_json(force=True)
        print("📥 Raw received data:", data)  # ADD THIS

        jd_id = data.get("jd_id")
        weights = data.get("weights")
        time_slots = data.get("time_slots")

        if not jd_id or not weights or not time_slots:
            print("❌ Missing fields in request")
            return jsonify({"error": "Missing fields in request"}), 400

        print(f"📩 Received config for JD {jd_id}")
        print(f"🔧 Weights: {weights}")
        print(f"⏰ Time Slots: {time_slots}")

        # Convert to JSON strings
        weights_json = json.dumps(weights)
        time_slots_json = json.dumps(time_slots)

        conn = sqlite3.connect("jd_analysis.db")
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jd_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jd_id INTEGER,
                weights TEXT,
                time_slots TEXT
            )
        """)

        # Insert config
        cursor.execute("""
            INSERT INTO jd_config (jd_id, weights, time_slots)
            VALUES (?, ?, ?)
        """, (jd_id, weights_json, time_slots_json))

        conn.commit()
        conn.close()

        print(f"✅ Successfully saved config for JD {jd_id}")
        return jsonify({"message": "Config saved successfully"}), 200

    except Exception as e:
        print(f"❌ Error saving config: {e}")
        return jsonify({"error": str(e)}), 500

    
@app.route('/api/get_all_candidates', methods=['GET'])
def get_all_candidates():
    """
    Route to fetch all candidates from the database.
    """
    try:
        conn = sqlite3.connect("jd_analysis.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM candidates")
        candidates = cursor.fetchall()

        # Convert the fetched data into a list of dictionaries
        candidate_list = []
        for candidate in candidates:
            candidate_dict = {
                "candidate_id": candidate[1],
                "name": candidate[2],
                "email": candidate[3],
                "skills": candidate[4],
                "work_experience": candidate[5],
                "education_degree": candidate[6],
                "education_university": candidate[7],
                "education_year": candidate[8],
                "certifications": candidate[9],
                "achievements": candidate[10]
            }
            candidate_list.append(candidate_dict)

        conn.close()
        return jsonify(candidate_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/get_all_configs', methods=['GET'])
def get_all_configs():
    try:
        conn = sqlite3.connect("jd_analysis.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = '''
        SELECT j.job_id, j.title, c.weights, c.time_slots
        FROM job_descriptions j
        JOIN jd_config c ON j.job_id = c.jd_id
        '''
        rows = cursor.execute(query).fetchall()

        configs = []
        for row in rows:
            configs.append({
                "jd_id": row["job_id"],
                "title": row["title"],
                "weights": json.loads(row["weights"]),
                "time_slots": json.loads(row["time_slots"]),
            })

        conn.close()
        return jsonify(configs), 200
    except Exception as e:
        print("❌ Error fetching configurations:", str(e))
        return jsonify({"error": str(e)}), 500



def extract_text_from_pdf(pdf_file):
    # Logic to extract text from the PDF (using pdfplumber or PyMuPDF)
    import pdfplumber
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

@app.route('/api/jd_candidates', methods=['GET'])
def get_jd_candidates():
    conn = sqlite3.connect('jd_analysis.db')
    cursor = conn.cursor()

    # Get all job descriptions with UUID job_id
    cursor.execute("SELECT job_id, title FROM job_descriptions")
    jds = cursor.fetchall()

    results = []

    for jd in jds:
        job_id, title = jd

        # Join matches with candidates using UUIDs
        cursor.execute("""
            SELECT c.email, m.score 
            FROM jd_candidate_matches m
            JOIN candidates c ON m.candidate_id = c.candidate_id
            WHERE m.jd_id = ?
        """, (job_id,))
        matches = cursor.fetchall()

        match_data = []
        for email, score in matches:
            match_data.append({
                'candidate_email': email,
                'match_score': score
            })

        results.append({
            'jd_id': job_id,
            'title': title,
            'candidates': match_data if match_data else None
        })
        process_match_scores(results)

    conn.close()
    return jsonify(results)



@app.route('/api/match_candidates', methods=['POST'])
def match_candidates():
    try:
        data = request.get_json()
        print("Received data:", data)  # Add this line

        jd_id = data['jd_id']

        # Fetch JD details
        conn = sqlite3.connect("jd_analysis.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM job_descriptions WHERE job_id = ?", (jd_id,))
        jd_row = cursor.fetchone()
        if not jd_row:
            return jsonify({"error": "JD not found"}), 404

        jd_data = {
            "job_id": jd_row[1],
            "title": jd_row[2],
            "education_degree": jd_row[3],
            "education_field": jd_row[4],
            "programming_languages": jd_row[5].split(', '),
            "tools_and_technologies": jd_row[6].split(', '),
            "soft_skills": jd_row[7].split(', '),
            "responsibilities": json.loads(jd_row[8]),
            "experience_years": jd_row[9],
            "experience_domains": jd_row[10].split(', ')
        }

        # Fetch all candidates
        cursor.execute("SELECT * FROM candidates")
        candidates = cursor.fetchall()
        candidate_data = []
        for row in candidates:
            candidate_data.append({
                "candidate_id": row[1],
                "name": row[2],
                "email": row[3],
                "skills": row[4].split(', '),
                "work_experience": json.loads(row[5]),
                "education": {
                    "degree": row[6],
                    "university": row[7],
                    "year": row[8]
                },
                "certifications": json.loads(row[9]),
                "achievements": json.loads(row[10])
            })

        # Call your agent
        from retail_mas_demo.agents.matcher import MatchingAgent
        matcher = MatchingAgent()
                # Ensure the matches table exists

        results = matcher.match(jd_data, candidate_data)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jd_candidate_matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jd_id TEXT,
                candidate_id TEXT,
                score INTEGER
            )
        ''')

        # Insert match results into the database
        for match in results:
            cursor.execute('''
                INSERT INTO jd_candidate_matches (jd_id, candidate_id, score)
                VALUES (?, ?, ?)
            ''', (match['jd_id'], match['candidate_id'], match['score']))

        conn.commit()
        conn.close()

        return jsonify(results), 200

    except Exception as e:
        print(f"Error in matching candidates: {e}")
        return jsonify({"error": str(e)}), 500


def process_match_scores(results):
    high = []
    medium = []
    low = []

    for jd in results:
        for candidate in jd['candidates'] or []:
            score = candidate['match_score']
            if score > 80:
                high.append(candidate)
            elif score > 60:
                medium.append(candidate)
            else:
                low.append(candidate)

    # Route to appropriate functions
    process_high_matches(high)
    process_medium_matches(medium)
    process_low_matches(low)

def process_high_matches(candidates):
    print("🔥 High matches (score > 80):")
    for c in candidates:
        email = c['candidate_email']
        score = c['match_score']

        print(f"{email} - {score}")
        send_selection_email(email, score)

def process_medium_matches(candidates):
    print("🟡 Medium matches (score 61–80):")
    for c in candidates:
        email = c['candidate_email']
        score = c['match_score']

        print(f"{email} - {score}")
        send_assessment_email(email, score)

def process_low_matches(candidates):
    print("🧊 Low matches (score ≤ 60):")
    for c in candidates:
        email = c['candidate_email']
        score = c['match_score']

        print(f"{email} - {score}")
        send_rejection_email(email, score)



def send_selection_email(candidate_email, match_score):
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg['Subject'] = '🎉 You have been selected!'
    msg['From'] = 'your_email@gmail.com'
    msg['To'] = 'harshalmwagh2005@gmail.com'  # override for testing

    msg.set_content(f"""
Hi,

Congratulations! Based on your profile and the job description, you have been selected with a match score of {match_score}.

We'll contact you soon for the next steps.

Best,
HR Team
""")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('h233068@gmail.com', 'zjpe fvco fuqg xxpr')
            smtp.send_message(msg)
            print(f"✅ Email sent for candidate {candidate_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {candidate_email} - {e}")


def send_assessment_email(candidate_email, match_score):
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg['Subject'] = '📝 Take the Next Step: Short Assessment Required'
    msg['From'] = 'your_email@gmail.com'
    msg['To'] = 'harshalmwagh2005@gmail.com'  # override for testing

    msg.set_content(f"""
Hi,

Thank you for your interest in the role.

Based on your profile and the job description, you've received a **match score of {match_score}**, which qualifies you for the next step in our process.

📝 We'd like you to take a short assessment to help us evaluate your fit further.

Please expect a follow-up email with the quiz link shortly.

All the best,  
HR Team
""")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('h233068@gmail.com', 'zjpe fvco fuqg xxpr')
            smtp.send_message(msg)
            print(f"✅ Quiz invitation email sent to {candidate_email}")
    except Exception as e:
        print(f"❌ Failed to send quiz invitation to {candidate_email} - {e}")

def send_rejection_email(candidate_email, match_score):
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg['Subject'] = 'Update on Your Application'
    msg['From'] = 'your_email@gmail.com'
    msg['To'] = 'harshalmwagh2005@gmail.com'  # override for testing

    msg.set_content(f"""
Hi,

Thank you for applying.

After reviewing your profile, you received a **match score of {match_score}** for this position. Unfortunately, we will not be moving forward with your application at this time.

We appreciate your interest and encourage you to apply for future opportunities with us.

Warm regards,  
HR Team
""")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('h233068@gmail.com', 'zjpe fvco fuqg xxpr')
            smtp.send_message(msg)
            print(f"✅ Rejection email sent to {candidate_email}")
    except Exception as e:
        print(f"❌ Failed to send rejection email to {candidate_email} - {e}")



if __name__ == '__main__':
    app.run(debug=True, port=5000)



