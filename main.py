"""
Auto Answer Script Correction System - CLI Entry Point
Reads answer key and student answers from JSON files,
grades them, and generates reports.
"""

import json
import os
import sys

from corrector.mcq_corrector import MCQCorrector
from corrector.subjective_corrector import SubjectiveCorrector
from corrector.report_generator import ReportGenerator


def load_json(filepath):
    """Load and return JSON data from a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def grade_student(student, answer_key, mcq_corrector, subj_corrector, report_gen):
    """Grade a single student and return the report data."""
    mcq_results = mcq_corrector.grade_all(student["answers"], answer_key["questions"])
    subj_results = subj_corrector.grade_all(student["answers"], answer_key["questions"])

    student_info = {
        "name": student["name"],
        "roll_number": student["roll_number"],
    }

    report_data = report_gen.generate_student_report(
        student_info, mcq_results, subj_results, answer_key["subject"]
    )
    return report_data


def main():
    """Main function to run the auto correction system."""
    # File paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    answer_key_path = os.path.join(base_dir, "data", "answer_key.json")
    student_answers_path = os.path.join(base_dir, "data", "student_answers.json")
    reports_dir = os.path.join(base_dir, "reports")

    # Check files exist
    if not os.path.exists(answer_key_path):
        print(f"Error: Answer key not found at {answer_key_path}")
        sys.exit(1)
    if not os.path.exists(student_answers_path):
        print(f"Error: Student answers not found at {student_answers_path}")
        sys.exit(1)

    # Load data
    print("Loading answer key and student answers...")
    answer_key = load_json(answer_key_path)
    student_data = load_json(student_answers_path)

    # Initialize correctors
    mcq_corrector = MCQCorrector()
    subj_corrector = SubjectiveCorrector()
    report_gen = ReportGenerator()

    print(f"\nSubject: {answer_key['subject']}")
    print(f"Total Questions: {len(answer_key['questions'])}")
    print(f"Total Students: {len(student_data['students'])}")
    print(f"\nGrading in progress...\n")

    # Grade each student
    all_reports = []
    for student in student_data["students"]:
        report_data = grade_student(student, answer_key, mcq_corrector, subj_corrector, report_gen)
        all_reports.append(report_data)

        # Print summary
        report_gen.print_summary(report_data)

        # Save HTML report
        filepath = report_gen.save_report(report_data, reports_dir)
        print(f"  Report saved: {filepath}")

    # Print class summary
    print(f"\n{'='*60}")
    print(f"  CLASS SUMMARY")
    print(f"{'='*60}")
    print(f"  {'Roll No':<12} {'Name':<20} {'Score':<12} {'%':<8} {'Grade'}")
    print(f"  {'-'*60}")
    for r in all_reports:
        s = r["summary"]
        st = r["student"]
        print(f"  {st['roll_number']:<12} {st['name']:<20} {s['total_score']}/{s['total_max']:<8} {s['percentage']:<8} {s['grade']}")
    print(f"{'='*60}")

    avg_percentage = sum(r["summary"]["percentage"] for r in all_reports) / len(all_reports) if all_reports else 0
    print(f"\n  Class Average: {avg_percentage:.1f}%")
    print(f"  Reports saved to: {reports_dir}/")
    print(f"\nDone! Open the HTML reports in a browser to view detailed results.")


if __name__ == "__main__":
    main()
