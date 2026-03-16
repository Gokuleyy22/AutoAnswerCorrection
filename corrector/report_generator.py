"""
Report Generator Module
Generates HTML and text reports for graded answer scripts.
"""

import os
from datetime import datetime


class ReportGenerator:
    """Generates grading reports in HTML format."""

    GRADE_THRESHOLDS = [
        (90, "A+"),
        (80, "A"),
        (70, "B+"),
        (60, "B"),
        (50, "C"),
        (40, "D"),
        (0, "F"),
    ]

    @staticmethod
    def get_grade(percentage):
        """Return letter grade based on percentage."""
        for threshold, grade in ReportGenerator.GRADE_THRESHOLDS:
            if percentage >= threshold:
                return grade
        return "F"

    def generate_student_report(self, student_info, mcq_results, subjective_results, subject):
        """
        Generate a complete grading report for one student.

        Returns:
            dict with summary and detailed results
        """
        all_results = mcq_results + subjective_results
        total_score = round(sum(r["score"] for r in all_results), 1)
        total_max = sum(r["max_marks"] for r in all_results)
        percentage = round((total_score / total_max) * 100, 1) if total_max > 0 else 0
        grade = self.get_grade(percentage)

        mcq_score = round(sum(r["score"] for r in mcq_results), 1)
        mcq_max = sum(r["max_marks"] for r in mcq_results)
        subj_score = round(sum(r["score"] for r in subjective_results), 1)
        subj_max = sum(r["max_marks"] for r in subjective_results)

        return {
            "student": student_info,
            "subject": subject,
            "summary": {
                "total_score": total_score,
                "total_max": total_max,
                "percentage": percentage,
                "grade": grade,
                "mcq_score": mcq_score,
                "mcq_max": mcq_max,
                "mcq_count": len(mcq_results),
                "subjective_score": subj_score,
                "subjective_max": subj_max,
                "subjective_count": len(subjective_results),
            },
            "mcq_results": mcq_results,
            "subjective_results": subjective_results,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    def generate_html_report(self, report_data):
        """Generate a standalone HTML report string."""
        student = report_data["student"]
        summary = report_data["summary"]

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Report - {student['name']} ({student['roll_number']})</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 30px; background: #f5f5f5; }}
        .container {{ max-width: 900px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #2980b9; margin-top: 30px; }}
        .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 15px 0; }}
        .info-item {{ padding: 8px 12px; background: #ecf0f1; border-radius: 5px; }}
        .info-label {{ font-weight: bold; color: #555; }}
        .summary-box {{ background: #e8f6ff; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center; }}
        .grade {{ font-size: 48px; font-weight: bold; color: #27ae60; }}
        .percentage {{ font-size: 24px; color: #2c3e50; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th {{ background: #3498db; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px 12px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f0f8ff; }}
        .correct {{ color: #27ae60; font-weight: bold; }}
        .incorrect {{ color: #e74c3c; font-weight: bold; }}
        .keyword-matched {{ color: #27ae60; }}
        .keyword-missing {{ color: #e74c3c; }}
        .score-bar {{ background: #ecf0f1; border-radius: 10px; height: 20px; overflow: hidden; }}
        .score-fill {{ background: #3498db; height: 100%; border-radius: 10px; transition: width 0.3s; }}
        .footer {{ text-align: center; color: #999; margin-top: 30px; font-size: 12px; }}
    </style>
</head>
<body>
<div class="container">
    <h1>Auto Answer Script Correction Report</h1>

    <div class="info-grid">
        <div class="info-item"><span class="info-label">Student Name:</span> {student['name']}</div>
        <div class="info-item"><span class="info-label">Roll Number:</span> {student['roll_number']}</div>
        <div class="info-item"><span class="info-label">Subject:</span> {report_data['subject']}</div>
        <div class="info-item"><span class="info-label">Date:</span> {report_data['generated_at']}</div>
    </div>

    <div class="summary-box">
        <div class="grade">Grade: {summary['grade']}</div>
        <div class="percentage">{summary['total_score']} / {summary['total_max']} ({summary['percentage']}%)</div>
        <p>MCQ: {summary['mcq_score']}/{summary['mcq_max']} | Subjective: {summary['subjective_score']}/{summary['subjective_max']}</p>
    </div>
"""

        # MCQ Results Table
        if report_data["mcq_results"]:
            html += """
    <h2>MCQ Questions</h2>
    <table>
        <tr><th>#</th><th>Question</th><th>Your Answer</th><th>Correct Answer</th><th>Result</th><th>Marks</th></tr>
"""
            for r in report_data["mcq_results"]:
                status_class = "correct" if r["is_correct"] else "incorrect"
                status_text = "Correct" if r["is_correct"] else "Wrong"
                html += f"""        <tr>
            <td>{r['question_id']}</td>
            <td>{r['question']}</td>
            <td>{r['student_answer']}</td>
            <td>{r['correct_answer']}</td>
            <td class="{status_class}">{status_text}</td>
            <td>{r['score']}/{r['max_marks']}</td>
        </tr>\n"""
            html += "    </table>\n"

        # Subjective Results
        if report_data["subjective_results"]:
            html += """
    <h2>Subjective Questions</h2>
"""
            for r in report_data["subjective_results"]:
                fill_width = (r["score"] / r["max_marks"] * 100) if r["max_marks"] > 0 else 0
                matched_html = ", ".join(
                    f'<span class="keyword-matched">{kw}</span>' for kw in r.get("matched_keywords", [])
                )
                missing_html = ", ".join(
                    f'<span class="keyword-missing">{kw}</span>' for kw in r.get("missing_keywords", [])
                )

                html += f"""
    <div style="background:#fafafa; padding:15px; border-radius:8px; margin:10px 0; border-left:4px solid #3498db;">
        <strong>Q{r['question_id']}. {r['question']}</strong> [{r['max_marks']} marks]
        <p><strong>Your Answer:</strong> {r['student_answer'] if r['student_answer'] else '<em>Not answered</em>'}</p>
        <div class="score-bar"><div class="score-fill" style="width:{fill_width}%"></div></div>
        <p><strong>Score:</strong> {r['score']}/{r['max_marks']} |
           Similarity: {r.get('similarity_score', 0)}% |
           Keyword Match: {r.get('keyword_score', 0)}%</p>
        <p><strong>Keywords Found:</strong> {matched_html if matched_html else 'None'}</p>
        <p><strong>Keywords Missing:</strong> {missing_html if missing_html else 'None'}</p>
    </div>
"""

        html += f"""
    <div class="footer">
        Generated by Auto Answer Script Correction System | {report_data['generated_at']}
    </div>
</div>
</body>
</html>"""
        return html

    def save_report(self, report_data, output_dir="reports"):
        """Save HTML report to file. Returns the file path."""
        os.makedirs(output_dir, exist_ok=True)
        student = report_data["student"]
        filename = f"report_{student['roll_number']}.html"
        filepath = os.path.join(output_dir, filename)

        html = self.generate_html_report(report_data)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        return filepath

    def print_summary(self, report_data):
        """Print a text summary to the console."""
        student = report_data["student"]
        summary = report_data["summary"]

        print(f"\n{'='*60}")
        print(f"  Student: {student['name']} ({student['roll_number']})")
        print(f"  Subject: {report_data['subject']}")
        print(f"{'='*60}")
        print(f"  MCQ Score:        {summary['mcq_score']} / {summary['mcq_max']}")
        print(f"  Subjective Score: {summary['subjective_score']} / {summary['subjective_max']}")
        print(f"  Total Score:      {summary['total_score']} / {summary['total_max']}")
        print(f"  Percentage:       {summary['percentage']}%")
        print(f"  Grade:            {summary['grade']}")
        print(f"{'='*60}\n")
