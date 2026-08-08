from flask import Flask, render_template, request
import sqlite3
import os
import PyPDF2

app = Flask(__name__)
app.config["UPLOAD_FOLDER"]="uploads"

def extract_text_from_pdf(pdf_path):

    text = ""

    with open(pdf_path, "rb") as file:

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            text += page.extract_text() or ""

    return text 


skills_list = [
    "Python",
    "Java",
    "C",
    "C++",
    "HTML",
    "CSS",
    "JavaScript",
    "SQL",
    "MySQL",
    "Flask",
    "Django",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "Pandas",
    "NumPy",
    "Git",
    "GitHub",
    "Data Analysis",
    "AI"
]

job_skills = {
    "Software Engineer": [
        "Python", "Java", "SQL", "Git", "HTML", "CSS", "JavaScript"
    ],

    "Python Developer": [
        "Python", "Flask", "SQL", "Git", "HTML", "CSS"
    ],

    "Web Developer": [
        "HTML", "CSS", "JavaScript", "SQL", "Git"
    ],

    "Data Analyst": [
        "Python", "SQL", "Pandas", "NumPy", "Data Analysis"
    ],

    "AI/ML Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "Pandas",
        "NumPy",
        "SQL",
        "Git"
    ]
}

def create_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            return render_template("dashboard.html")
        else:
            return "Invalid email or password"

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, password)
        )

        conn.commit()
        conn.close()

        return "Signup successful!"

    return render_template("signup.html")
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE users SET password=? WHERE email=?",
            (password, email)
        )

        conn.commit()
        conn.close()

        return "Password updated successfully! <br><br><a href='/'>Go to Login</a>"

    return render_template("forgot_password.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    resume = request.files["resume"]
    job_role = request.form["job_role"]

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], resume.filename)
    resume.save(file_path)

    resume_text = extract_text_from_pdf(file_path)

    found_skills = []

    for skill in skills_list:
        if skill.lower() in resume_text.lower():
            found_skills.append(skill)
        required_skills = job_skills.get(job_role, [])

        missing_skills = []

        for skill in required_skills:
             if skill not in found_skills:
              missing_skills.append(skill)

        matched_skills = 0

        for skill in required_skills:
          if skill in found_skills:
              matched_skills += 1

        if len(required_skills) > 0:
          match_percentage = int((matched_skills / len(required_skills)) * 100)
        else:
          match_percentage = 0

   
        return render_template(
          "results.html",
          job_role=job_role,
          found_skills=found_skills,
          missing_skills=missing_skills,
          match_percentage=match_percentage,
          recommendations=missing_skills
        )      

    
   
 
create_database()

if __name__ == "__main__":
    app.run(debug=True)