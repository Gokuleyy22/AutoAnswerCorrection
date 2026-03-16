"""
Auto Answer Script Correction System - Flask Web Application
Provides a web interface for uploading answer keys and student answers,
and viewing grading results.
"""

import json
import os

from flask import Flask, render_template, request, redirect, url_for, flash

from corrector.mcq_corrector import MCQCorrector
from corrector.subjective_corrector import SubjectiveCorrector
from corrector.report_generator import ReportGenerator

app = Flask(__name__)
app.secret_key = os.urandom(32)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Initialize correctors
mcq_corrector = MCQCorrector()
subj_corrector = SubjectiveCorrector()
report_gen = ReportGenerator()


def load_json_file(filepath):
    """Safely load JSON from a file path."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_answer_key(data):
    """Basic validation of answer key structure."""
    if "subject" not in data or "questions" not in data:
        return False, "Answer key must have 'subject' and 'questions' fields."
    for q in data["questions"]:
        if "id" not in q or "type" not in q or "question" not in q or "marks" not in q:
            return False, f"Question missing required fields (id, type, question, marks)."
        if q["type"] == "mcq" and "correct_answer" not in q:
            return False, f"MCQ question {q['id']} missing 'correct_answer'."
        if q["type"] == "subjective" and "model_answer" not in q:
            return False, f"Subjective question {q['id']} missing 'model_answer'."
    return True, "Valid"


def validate_student_answers(data):
    """Basic validation of student answers structure."""
    if "students" not in data:
        return False, "Student answers must have a 'students' field."
    for s in data["students"]:
        if "roll_number" not in s or "name" not in s or "answers" not in s:
            return False, "Each student must have 'roll_number', 'name', and 'answers'."
    return True, "Valid"


@app.route("/")
def index():
    """Home page with option to use sample data or upload custom data."""
    return render_template("index.html")


@app.route("/grade", methods=["POST"])
def grade():
    """Grade answers using uploaded or sample data."""
    use_sample = request.form.get("use_sample") == "yes"

    if use_sample:
        # Use sample data files
        ak_path = os.path.join(DATA_DIR, "answer_key.json")
        sa_path = os.path.join(DATA_DIR, "student_answers.json")

        if not os.path.exists(ak_path) or not os.path.exists(sa_path):
            flash("Sample data files not found in data/ directory.", "error")
            return redirect(url_for("index"))

        answer_key = load_json_file(ak_path)
        student_data = load_json_file(sa_path)
    else:
        # Use uploaded files
        ak_file = request.files.get("answer_key")
        sa_file = request.files.get("student_answers")

        if not ak_file or not sa_file:
            flash("Please upload both answer key and student answers files.", "error")
            return redirect(url_for("index"))

        if not ak_file.filename.endswith(".json") or not sa_file.filename.endswith(".json"):
            flash("Only JSON files are accepted.", "error")
            return redirect(url_for("index"))

        try:
            ak_content = ak_file.read().decode("utf-8")
            sa_content = sa_file.read().decode("utf-8")
            answer_key = json.loads(ak_content)
            student_data = json.loads(sa_content)
        except (json.JSONDecodeError, UnicodeDecodeError):
            flash("Invalid JSON file(s). Please check the format.", "error")
            return redirect(url_for("index"))

    # Validate data
    valid, msg = validate_answer_key(answer_key)
    if not valid:
        flash(f"Answer key error: {msg}", "error")
        return redirect(url_for("index"))

    valid, msg = validate_student_answers(student_data)
    if not valid:
        flash(f"Student answers error: {msg}", "error")
        return redirect(url_for("index"))

    # Grade all students
    all_reports = []
    for student in student_data["students"]:
        mcq_results = mcq_corrector.grade_all(student["answers"], answer_key["questions"])
        subj_results = subj_corrector.grade_all(student["answers"], answer_key["questions"])

        student_info = {
            "name": student["name"],
            "roll_number": student["roll_number"],
        }

        report_data = report_gen.generate_student_report(
            student_info, mcq_results, subj_results, answer_key["subject"]
        )
        all_reports.append(report_data)

        # Save HTML report
        report_gen.save_report(report_data, REPORTS_DIR)

    # Calculate class stats
    avg_percentage = sum(r["summary"]["percentage"] for r in all_reports) / len(all_reports) if all_reports else 0
    highest = max(all_reports, key=lambda r: r["summary"]["percentage"]) if all_reports else None
    lowest = min(all_reports, key=lambda r: r["summary"]["percentage"]) if all_reports else None

    class_stats = {
        "average": round(avg_percentage, 1),
        "highest": highest["summary"]["percentage"] if highest else 0,
        "lowest": lowest["summary"]["percentage"] if lowest else 0,
        "total_students": len(all_reports),
    }

    # Rank students by percentage (descending)
    all_reports.sort(key=lambda r: r["summary"]["percentage"], reverse=True)
    for rank, report in enumerate(all_reports, start=1):
        report["rank"] = rank

    return render_template("results.html", reports=all_reports, stats=class_stats, subject=answer_key["subject"])


@app.route("/create_questions")
def create_questions():
    """Page to create questions via a form and build the answer key JSON."""
    return render_template("create_questions.html")


@app.route("/grade_created", methods=["POST"])
def grade_created():
    """Grade student answers against a form-built answer key."""
    ak_json = request.form.get("answer_key_json", "")
    if not ak_json:
        flash("No questions were created. Please add at least one question.", "error")
        return redirect(url_for("create_questions"))

    try:
        answer_key = json.loads(ak_json)
    except json.JSONDecodeError:
        flash("Invalid answer key data. Please try again.", "error")
        return redirect(url_for("create_questions"))

    valid, msg = validate_answer_key(answer_key)
    if not valid:
        flash(f"Answer key error: {msg}", "error")
        return redirect(url_for("create_questions"))

    input_mode = request.form.get("student_input_mode", "file")

    if input_mode == "form":
        sa_json = request.form.get("student_answers_json", "")
        if not sa_json:
            flash("No student answers provided. Please add at least one student.", "error")
            return redirect(url_for("create_questions"))
        try:
            student_data = json.loads(sa_json)
        except json.JSONDecodeError:
            flash("Invalid student answers data.", "error")
            return redirect(url_for("create_questions"))
    else:
        sa_file = request.files.get("student_answers")
        if not sa_file:
            flash("Please upload a student answers JSON file.", "error")
            return redirect(url_for("create_questions"))

        if not sa_file.filename.endswith(".json"):
            flash("Only JSON files are accepted for student answers.", "error")
            return redirect(url_for("create_questions"))

        try:
            sa_content = sa_file.read().decode("utf-8")
            student_data = json.loads(sa_content)
        except (json.JSONDecodeError, UnicodeDecodeError):
            flash("Invalid student answers JSON file.", "error")
            return redirect(url_for("create_questions"))

    valid, msg = validate_student_answers(student_data)
    if not valid:
        flash(f"Student answers error: {msg}", "error")
        return redirect(url_for("create_questions"))

    # Grade all students
    all_reports = []
    for student in student_data["students"]:
        mcq_results = mcq_corrector.grade_all(student["answers"], answer_key["questions"])
        subj_results = subj_corrector.grade_all(student["answers"], answer_key["questions"])

        student_info = {
            "name": student["name"],
            "roll_number": student["roll_number"],
        }

        report_data = report_gen.generate_student_report(
            student_info, mcq_results, subj_results, answer_key["subject"]
        )
        all_reports.append(report_data)
        report_gen.save_report(report_data, REPORTS_DIR)

    avg_percentage = sum(r["summary"]["percentage"] for r in all_reports) / len(all_reports) if all_reports else 0
    highest = max(all_reports, key=lambda r: r["summary"]["percentage"]) if all_reports else None
    lowest = min(all_reports, key=lambda r: r["summary"]["percentage"]) if all_reports else None

    class_stats = {
        "average": round(avg_percentage, 1),
        "highest": highest["summary"]["percentage"] if highest else 0,
        "lowest": lowest["summary"]["percentage"] if lowest else 0,
        "total_students": len(all_reports),
    }

    # Rank students by percentage (descending)
    all_reports.sort(key=lambda r: r["summary"]["percentage"], reverse=True)
    for rank, report in enumerate(all_reports, start=1):
        report["rank"] = rank

    return render_template("results.html", reports=all_reports, stats=class_stats, subject=answer_key["subject"])


@app.route("/report/<roll_number>")
def view_report(roll_number):
    """View detailed report for a specific student."""
    report_path = os.path.join(REPORTS_DIR, f"report_{roll_number}.html")
    if not os.path.exists(report_path):
        flash(f"Report not found for {roll_number}.", "error")
        return redirect(url_for("index"))

    with open(report_path, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    os.makedirs(REPORTS_DIR, exist_ok=True)
    print("Starting Auto Answer Script Correction System...")
    print("Open http://127.0.0.1:5001 in your browser")
    print("From other devices on the same Wi-Fi: http://192.0.0.2:5001")
    app.run(debug=True, port=5001, host="0.0.0.0")
