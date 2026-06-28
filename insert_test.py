from db import conn, cursor

cursor.execute("""
INSERT INTO resume_analysis
(resume_name, ats_score, strengths, weaknesses, advice)
VALUES (%s,%s,%s,%s,%s)
""",
(
    "test.pdf",
    90,
    "Python, MySQL",
    "None",
    "Excellent Resume"
))

conn.commit()

print("Inserted Successfully")