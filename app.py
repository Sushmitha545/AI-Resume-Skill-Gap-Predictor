from flask import Flask, render_template, request
import sqlite3
import os
import PyPDF2

app = Flask(__name__)

app.config["UPLOAD_FOLDER"]="uploads"
os.makedirs(app.config["UPLOAD_FOLDER"],
            exist_ok=True)

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

    # 💻 SOFTWARE & DEVELOPMENT
    "Software Engineer": [
        "Python", "Java", "SQL", "Git", "HTML", "CSS", "JavaScript"
    ],

    "Python Developer": [
        "Python", "Flask", "Django", "SQL", "Git", "HTML", "CSS"
    ],

    "Java Developer": [
        "Java", "SQL", "Git", "Spring", "HTML", "CSS", "JavaScript"
    ],

    "C/C++ Developer": [
        "C", "C++", "Git", "Data Structures", "Algorithms"
    ],

    "Full Stack Developer": [
        "HTML", "CSS", "JavaScript", "Python", "Flask",
        "SQL", "Git", "React"
    ],

    "Frontend Developer": [
        "HTML", "CSS", "JavaScript", "React", "Git"
    ],

    "Backend Developer": [
        "Python", "Flask", "Django", "Java", "SQL", "Git", "REST API"
    ],

    "Web Developer": [
        "HTML", "CSS", "JavaScript", "SQL", "Git"
    ],

    "Mobile App Developer": [
        "Java", "Kotlin", "Android", "Git", "SQL"
    ],

    "DevOps Engineer": [
        "Linux", "Git", "Docker", "CI/CD", "Python",
        "AWS", "Kubernetes"
    ],

    "Software Tester / QA": [
        "Testing", "Python", "Java", "SQL", "Selenium", "Git"
    ],


    # 🤖 AI & DATA
    "AI Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "TensorFlow", "Pandas", "NumPy", "AI"
    ],

    "AI/ML Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "TensorFlow", "Pandas", "NumPy", "AI"
    ],

    "Machine Learning Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "TensorFlow", "Pandas", "NumPy", "Git"
    ],

    "Data Scientist": [
        "Python", "Machine Learning", "Pandas",
        "NumPy", "SQL", "Data Analysis", "Statistics"
    ],

    "Data Analyst": [
        "Python", "SQL", "Pandas", "NumPy",
        "Data Analysis", "Excel", "Statistics"
    ],

    "Data Engineer": [
        "Python", "SQL", "Data Engineering",
        "Pandas", "Git", "AWS"
    ],

    "NLP Engineer": [
        "Python", "NLP", "Machine Learning",
        "Deep Learning", "TensorFlow"
    ],

    "Computer Vision Engineer": [
        "Python", "Computer Vision",
        "Machine Learning", "Deep Learning",
        "TensorFlow", "OpenCV"
    ],


    # 🔐 CYBERSECURITY
    "Cybersecurity Analyst": [
        "Cybersecurity", "Networking", "Linux",
        "Python", "Cryptography", "SQL"
    ],

    "Security Engineer": [
        "Cybersecurity", "Networking", "Linux",
        "Python", "Cryptography"
    ],

    "Ethical Hacker": [
        "Cybersecurity", "Linux", "Networking",
        "Python", "Ethical Hacking", "Cryptography"
    ],

    "SOC Analyst": [
        "Cybersecurity", "Networking", "Linux",
        "SIEM", "Threat Analysis"
    ],

    "Information Security Analyst": [
        "Cybersecurity", "Networking", "Linux",
        "Risk Management", "Cryptography"
    ],


    # ☁️ CLOUD & INFRASTRUCTURE
    "Cloud Engineer": [
        "AWS", "Azure", "Linux", "Python",
        "Docker", "Networking", "Git"
    ],

    "Cloud Architect": [
        "AWS", "Azure", "Cloud Computing",
        "Networking", "Linux", "Docker"
    ],

    "AWS Engineer": [
        "AWS", "Linux", "Python", "Docker",
        "Networking", "Git"
    ],

    "System Administrator": [
        "Linux", "Windows", "Networking",
        "Python", "Security"
    ],

    "Network Engineer": [
        "Networking", "Linux", "Cybersecurity",
        "Cloud Computing"
    ],


    # 🎨 DESIGN
    "UI/UX Designer": [
        "UI/UX", "Figma", "Wireframing",
        "Prototyping", "User Research"
    ],

    "Graphic Designer": [
        "Graphic Design", "Photoshop",
        "Illustrator", "Canva", "Typography"
    ],

    "Product Designer": [
        "UI/UX", "Figma", "Prototyping",
        "User Research", "Product Design"
    ],


    # 📊 BUSINESS
    "Business Analyst": [
        "Business Analysis", "SQL", "Excel",
        "Data Analysis", "Communication"
    ],

    "Project Manager": [
        "Project Management", "Leadership",
        "Communication", "Agile", "Risk Management"
    ],

    "Product Manager": [
        "Product Management", "Leadership",
        "Communication", "Agile", "Market Research"
    ],

    "Digital Marketing Specialist": [
        "Digital Marketing", "SEO", "Social Media",
        "Content Marketing", "Google Analytics"
    ],

    "HR Specialist": [
        "Human Resources", "Recruitment",
        "Communication", "Leadership", "Management"
    ],


    # 💰 FINANCE
    "Financial Analyst": [
        "Financial Analysis", "Excel",
        "Accounting", "Statistics", "Data Analysis"
    ],

    "Accountant": [
        "Accounting", "Finance", "Excel",
        "Taxation", "Financial Analysis"
    ],

    "Banking Associate": [
        "Finance", "Accounting", "Communication",
        "Excel", "Customer Service"
    ],


    # 🧪 ENGINEERING
    "Electronics Engineer": [
        "Electronics", "C", "C++",
        "Embedded Systems", "Microcontrollers"
    ],

    "Mechanical Engineer": [
        "Mechanical Engineering", "CAD",
        "AutoCAD", "Design", "Manufacturing"
    ],

    "Civil Engineer": [
        "Civil Engineering", "AutoCAD",
        "Construction", "Structural Design"
    ],

    "Biomedical Engineer": [
        "Biomedical Engineering",
        "Medical Technology", "Research",
        "Data Analysis"
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