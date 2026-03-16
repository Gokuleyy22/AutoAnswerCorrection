"""
MCQ Corrector Module
Handles grading of multiple-choice questions by exact match.
"""


class MCQCorrector:
    """Grades MCQ answers by comparing against the answer key."""

    def grade(self, student_answer, correct_answer, marks):
        """
        Grade a single MCQ question.

        Returns:
            dict with 'score', 'max_marks', 'is_correct'
        """
        is_correct = student_answer.strip().upper() == correct_answer.strip().upper()
        return {
            "score": marks if is_correct else 0,
            "max_marks": marks,
            "is_correct": is_correct,
        }

    def grade_all(self, student_answers, answer_key_questions):
        """
        Grade all MCQ questions for a student.

        Args:
            student_answers: list of {"question_id": int, "answer": str}
            answer_key_questions: list of question dicts from answer key

        Returns:
            list of result dicts
        """
        # Build lookup: question_id -> student_answer
        answer_map = {a["question_id"]: a["answer"] for a in student_answers}

        results = []
        for q in answer_key_questions:
            if q["type"] != "mcq":
                continue

            student_ans = answer_map.get(q["id"], "")
            result = self.grade(student_ans, q["correct_answer"], q["marks"])
            result["question_id"] = q["id"]
            result["question"] = q["question"]
            result["student_answer"] = student_ans
            result["correct_answer"] = q["correct_answer"]
            result["type"] = "mcq"
            results.append(result)

        return results
