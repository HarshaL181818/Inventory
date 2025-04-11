import sqlite3

conn = sqlite3.connect("jd_analysis.db")
cursor = conn.cursor()

cursor.execute("select * from job_descriptions where job_id='e2734cbb-98fd-4036-a0c8-331fef1de88b'")
print(cursor.fetchall())

conn.commit()
conn.close()

print("✅ jd_configurations table created.")
