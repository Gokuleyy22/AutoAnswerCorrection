"""
Subjective Answer Corrector Module
Uses NLP-based text similarity and keyword matching to grade descriptive answers.
"""

from .text_similarity import TextSimilarity


class SubjectiveCorrector:
    """Grades subjective/descriptive answers using NLP techniques."""

    # Weight distribution for scoring
    SIMILARITY_WEIGHT = 0.6
    KEYWORD_WEIGHT = 0.4

    def __init__(self):
        self.similarity = TextSimilarity()

    def grade(self, student_answer, model_answer, keywords, marks):
        """
        Grade a single subjective question.

        Scoring:
            - 60% from TF-IDF cosine similarity with model answer
            - 40% from keyword match ratio

        Returns:
            dict with score breakdown
        """
        if not student_answer or not student_answer.strip():
            return {
                "score": 0,
                "max_marks": marks,
                "similarity_score": 0.0,
                "keyword_score": 0.0,
                "matched_keywords": [],
                "missing_keywords": keywords if keywords else [],
            }

        # Compute cosine similarity
        sim_score = self.similarity.cosine_sim(model_answer, student_answer)

        # Compute keyword match
        kw_score = self.similarity.keyword_match_score(student_answer, keywords)

        # Find matched and missing keywords
        student_lower = student_answer.lower()
        matched_keywords = [kw for kw in keywords if kw.lower() in student_lower]
        missing_keywords = [kw for kw in keywords if kw.lower() not in student_lower]

        # Combined weighted score
        combined = (sim_score * self.SIMILARITY_WEIGHT) + (kw_score * self.KEYWORD_WEIGHT)
        final_score = round(combined * marks, 1)

        # Cap at max marks
        final_score = min(final_score, marks)

        return {
            "score": final_score,
            "max_marks": marks,
            "similarity_score": round(sim_score * 100, 1),
            "keyword_score": round(kw_score * 100, 1),
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
        }

    def grade_all(self, student_answers, answer_key_questions):
        """
        Grade all subjective questions for a student.

        Args:
            student_answers: list of {"question_id": int, "answer": str}
            answer_key_questions: list of question dicts from answer key

        Returns:
            list of result dicts
        """
        answer_map = {a["question_id"]: a["answer"] for a in student_answers}

        results = []
        for q in answer_key_questions:
            if q["type"] != "subjective":
                continue

            student_ans = answer_map.get(q["id"], "")
            result = self.grade(
                student_ans,
                q["model_answer"],
                q.get("keywords", []),
                q["marks"],
            )
            result["question_id"] = q["id"]
            result["question"] = q["question"]
            result["student_answer"] = student_ans
            result["model_answer"] = q["model_answer"]
            result["type"] = "subjective"
            results.append(result)

        return results
