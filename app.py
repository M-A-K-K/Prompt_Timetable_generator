import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


api_key = os.getenv("OPENAI_API_KEY")
api_url = 'https://api.openai.com/v1/chat/completions'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}


def generate_study_timetable(data):
    prompt = f"""
    Develop a comprehensive and personalized study timetable for a student based on the following information:

    - **Name:** {data['name']}
    - **Field of Study:** {data['field_of_study']}
    - **Year of Study:** {data['year_of_study']}
    - **List of Subjects:** {data['subjects']}
    - **Preferred Learning Styles:** {data['learning_styles']}
    - **Personal Objectives:** {data['personal_objectives']}
    - **Challenges:** {data['challenges']}
    - **Extracurricular Activities:** {data['extracurricular_activities']}

    Create a detailed study plan that includes:
    1. **Subject Allocation:** Prioritize subjects based on difficulty and objectives.
    2. **Learning Style Adaptation:** Tailor study methods to the student's learning preferences.
    3. **Personal Objectives:** Align the study plan with the student’s goals.
    4. **Challenges:** Address any specific learning challenges.
    5. **Extracurricular Activities:** Balance study time with extracurricular commitments.
    6. **Weekly and Daily Breakdown:** Provide a weekly overview and daily schedule.
    7. **Regular Review:** Include intervals for progress review and timetable adjustment.

    Ensure the timetable is clear, flexible, and accommodates the student’s needs.
    """

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json={
                "model": "gpt-4o-mini",  
                "messages": [
                    {"role": "system", "content": "You are a professional timetable planner."},
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 600,
                "temperature": 0.7
            }
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except requests.exceptions.RequestException as e:
        print(f"Error generating timetable: {e}")
        return "An error occurred while generating the timetable. Please try again later."

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        
        students = []
        student_count = int(request.form["student_count"])

        for i in range(student_count):
            student_data = {
                "name": request.form[f"name_{i}"],
                "field_of_study": request.form[f"field_of_study_{i}"],
                "year_of_study": request.form[f"year_of_study_{i}"],
                "subjects": request.form[f"subjects_{i}"],
                "learning_styles": request.form[f"learning_styles_{i}"],
                "personal_objectives": request.form[f"personal_objectives_{i}"],
                "challenges": request.form[f"challenges_{i}"],
                "extracurricular_activities": request.form[f"extracurricular_activities_{i}"],
            }
            students.append(student_data)

        
        timetables = [generate_study_timetable(student) for student in students]

        
        return render_template("index.html", timetables=timetables)

    return render_template("index.html", timetables=None)

if __name__ == "__main__":
    app.run(debug=True)
