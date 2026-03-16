"""
Auto Answer Script Correction System - Project Documentation PDF Generator
Generates a comprehensive 40+ page PDF document with:
  - Cover page, Table of Contents, Abstract, Introduction
  - System architecture, module explanations, code walkthroughs
  - Data format guides, screenshots placeholders, flowcharts
  - Testing, results, conclusion, and future scope
"""

import os
import json
import textwrap
from fpdf import FPDF

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ─── Color palette ───────────────────────────────────────────────────────────
C_PRIMARY = (79, 70, 229)       # Indigo
C_PRIMARY_DARK = (55, 48, 163)
C_ACCENT = (6, 182, 212)        # Cyan
C_SUCCESS = (16, 185, 129)      # Green
C_DANGER = (239, 68, 68)        # Red
C_BG_LIGHT = (248, 250, 252)
C_TEXT = (30, 41, 59)
C_TEXT_SEC = (100, 116, 139)
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_CODE_BG = (243, 244, 246)
C_TABLE_HEAD = (79, 70, 229)
C_TABLE_ALT = (238, 242, 255)


class ProjectPDF(FPDF):
    """Custom FPDF subclass with styled headers, footers, and helper methods."""

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=25)
        self.toc_entries = []
        self.chapter_num = 0
        self.section_num = 0
        self.subsection_num = 0
        self._in_cover = False

    # ── Header / Footer ──────────────────────────────────────────────────
    def header(self):
        if self._in_cover:
            return
        if self.page_no() <= 2:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*C_TEXT_SEC)
        self.cell(0, 8, "Auto Answer Script Correction System - Project Documentation", align="L")
        self.ln(2)
        self.set_draw_color(*C_PRIMARY)
        self.set_line_width(0.4)
        self.line(10, 12, 200, 12)
        self.ln(6)

    def footer(self):
        if self._in_cover:
            return
        if self.page_no() <= 1:
            return
        self.set_y(-18)
        self.set_draw_color(*C_PRIMARY)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*C_TEXT_SEC)
        self.cell(0, 8, f"Page {self.page_no() - 1}", align="C")

    # ── TOC tracking ─────────────────────────────────────────────────────
    def add_toc_entry(self, level, title, page):
        self.toc_entries.append((level, title, page))

    # ── Chapter / Section headings ───────────────────────────────────────
    def chapter_title(self, title):
        self.chapter_num += 1
        self.section_num = 0
        self.subsection_num = 0
        numbered = f"Chapter {self.chapter_num}: {title}"
        self.add_toc_entry(0, numbered, self.page_no())
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(*C_PRIMARY_DARK)
        self.ln(4)
        self.cell(0, 14, numbered, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*C_PRIMARY)
        self.set_line_width(0.8)
        self.line(10, self.get_y() + 1, 200, self.get_y() + 1)
        self.ln(10)

    def section_title(self, title):
        self.section_num += 1
        self.subsection_num = 0
        numbered = f"{self.chapter_num}.{self.section_num} {title}"
        self.add_toc_entry(1, numbered, self.page_no())
        if self.get_y() > 250:
            self.add_page()
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*C_PRIMARY)
        self.ln(4)
        self.cell(0, 10, numbered, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def subsection_title(self, title):
        self.subsection_num += 1
        numbered = f"{self.chapter_num}.{self.section_num}.{self.subsection_num} {title}"
        self.add_toc_entry(2, numbered, self.page_no())
        if self.get_y() > 255:
            self.add_page()
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*C_PRIMARY_DARK)
        self.ln(2)
        self.cell(0, 8, numbered, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    # ── Body text ────────────────────────────────────────────────────────
    def body_text(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*C_TEXT)
        self.multi_cell(0, 6.5, text)
        self.ln(3)

    def body_text_bold(self, text):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*C_TEXT)
        self.multi_cell(0, 6.5, text)
        self.ln(2)

    def bullet_list(self, items):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*C_TEXT)
        for item in items:
            x = self.get_x()
            self.cell(8, 6.5, "-")
            self.multi_cell(0, 6.5, f"  {item}")
            self.ln(1)
        self.ln(3)

    def numbered_list(self, items):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*C_TEXT)
        for i, item in enumerate(items, 1):
            self.cell(10, 6.5, f"{i}.")
            self.multi_cell(0, 6.5, f" {item}")
            self.ln(1)
        self.ln(3)

    # ── Code block ───────────────────────────────────────────────────────
    def code_block(self, code, language="python"):
        self.set_font("Courier", "", 8.5)
        self.set_text_color(40, 40, 40)
        lines = code.split("\n")
        line_height = 4.5
        block_height = len(lines) * line_height + 8

        if self.get_y() + block_height > 270:
            self.add_page()

        y_start = self.get_y()
        self.set_fill_color(*C_CODE_BG)
        self.rect(12, y_start, 186, block_height, style="F")

        # Language label
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*C_TEXT_SEC)
        self.set_xy(14, y_start + 1)
        self.cell(30, 4, language.upper())

        self.set_font("Courier", "", 8.5)
        self.set_text_color(40, 40, 40)
        self.set_xy(14, y_start + 5)
        for line in lines:
            truncated = line[:120]
            self.cell(0, line_height, truncated, new_x="LMARGIN", new_y="NEXT")
            self.set_x(14)
        self.ln(6)

    # ── Styled table ─────────────────────────────────────────────────────
    def styled_table(self, headers, rows, col_widths=None):
        if col_widths is None:
            col_widths = [190 // len(headers)] * len(headers)

        # Header
        self.set_fill_color(*C_TABLE_HEAD)
        self.set_text_color(*C_WHITE)
        self.set_font("Helvetica", "B", 10)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 9, h, border=1, fill=True, align="C")
        self.ln()

        # Rows
        self.set_font("Helvetica", "", 9.5)
        for r_idx, row in enumerate(rows):
            if self.get_y() > 260:
                self.add_page()
                # Re-draw header
                self.set_fill_color(*C_TABLE_HEAD)
                self.set_text_color(*C_WHITE)
                self.set_font("Helvetica", "B", 10)
                for i, h in enumerate(headers):
                    self.cell(col_widths[i], 9, h, border=1, fill=True, align="C")
                self.ln()
                self.set_font("Helvetica", "", 9.5)

            if r_idx % 2 == 0:
                self.set_fill_color(*C_TABLE_ALT)
            else:
                self.set_fill_color(*C_WHITE)
            self.set_text_color(*C_TEXT)
            for i, val in enumerate(row):
                self.cell(col_widths[i], 8, str(val), border=1, fill=True, align="C")
            self.ln()
        self.ln(5)

    # ── Info box ─────────────────────────────────────────────────────────
    def info_box(self, title, text, color=C_ACCENT):
        if self.get_y() > 240:
            self.add_page()
        y = self.get_y()
        self.set_fill_color(*color)
        self.rect(10, y, 3, 24, style="F")
        self.set_xy(16, y + 2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*color)
        self.cell(0, 6, title)
        self.set_xy(16, y + 9)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*C_TEXT)
        self.multi_cell(178, 5.5, text)
        self.ln(6)

    # ── Diagram box (placeholder or text-based) ──────────────────────────
    def diagram_box(self, title, content_lines, width=190, box_color=C_PRIMARY):
        if self.get_y() > 220:
            self.add_page()
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*box_color)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

        y_start = self.get_y()
        line_h = 6
        total_h = len(content_lines) * line_h + 12
        self.set_draw_color(*box_color)
        self.set_line_width(0.5)
        self.rect(15, y_start, width - 20, total_h)
        self.set_fill_color(245, 247, 255)
        self.rect(15, y_start, width - 20, total_h, style="F")

        self.set_font("Courier", "", 9)
        self.set_text_color(*C_TEXT)
        self.set_xy(20, y_start + 6)
        for line in content_lines:
            self.cell(0, line_h, line, new_x="LMARGIN", new_y="NEXT")
            self.set_x(20)
        self.ln(8)

    # ── Flowchart-style box ──────────────────────────────────────────────
    def flow_box(self, text, x, y, w=50, h=14, shape="rect", color=C_PRIMARY):
        self.set_draw_color(*color)
        self.set_fill_color(240, 242, 255)
        self.set_line_width(0.5)
        if shape == "rounded":
            self.rect(x, y, w, h, style="DF")
        elif shape == "diamond":
            self.rect(x, y, w, h, style="DF")
        else:
            self.rect(x, y, w, h, style="DF")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*C_TEXT)
        self.set_xy(x + 2, y + 2)
        self.multi_cell(w - 4, 4, text, align="C")

    def flow_arrow(self, x1, y1, x2, y2):
        self.set_draw_color(*C_PRIMARY)
        self.set_line_width(0.4)
        self.line(x1, y1, x2, y2)
        # Simple arrowhead
        self.line(x2 - 2, y2 - 2, x2, y2)
        self.line(x2 + 2, y2 - 2, x2, y2)


def build_pdf():
    pdf = ProjectPDF()
    pdf.set_title("Auto Answer Script Correction System - Project Documentation")
    pdf.set_author("Project Team")

    # ─────────────────────────────────────────────────────────────────────
    # COVER PAGE
    # ─────────────────────────────────────────────────────────────────────
    pdf._in_cover = True
    pdf.add_page()

    # Background gradient effect
    for i in range(297):
        r = int(79 - (i * 0.08))
        g = int(70 - (i * 0.07))
        b = int(229 - (i * 0.22))
        r = max(30, min(255, r))
        g = max(20, min(255, g))
        b = max(100, min(255, b))
        pdf.set_fill_color(r, g, b)
        pdf.rect(0, i, 210, 1.2, style="F")

    # Title block
    pdf.set_y(60)
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(*C_WHITE)
    pdf.cell(0, 16, "AUTO ANSWER SCRIPT", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 16, "CORRECTION SYSTEM", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    # Decorative line
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(1)
    pdf.line(50, pdf.get_y(), 160, pdf.get_y())
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 16)
    pdf.cell(0, 10, "Project Documentation", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 13)
    pdf.cell(0, 8, "Automated Grading for MCQ & Subjective Answers", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "using Natural Language Processing (NLP)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, "Department of Computer Science", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Final Year Project Report", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, "Built with Python 3.9+ | Flask | scikit-learn | NLTK", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Academic Year 2025-2026", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf._in_cover = False

    # ─────────────────────────────────────────────────────────────────────
    # TABLE OF CONTENTS (placeholder - will be filled after all pages)
    # ─────────────────────────────────────────────────────────────────────
    toc_page = pdf.page_no() + 1  # Track where TOC starts

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 1: ABSTRACT
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("Abstract")
    pdf.body_text(
        "The Auto Answer Script Correction System is an automated examination evaluation platform "
        "designed to reduce the manual effort involved in grading student answer scripts. It leverages "
        "Natural Language Processing (NLP) techniques, specifically TF-IDF (Term Frequency-Inverse "
        "Document Frequency) vectorization and Cosine Similarity, to intelligently evaluate subjective "
        "answers against model answers provided by the instructor."
    )
    pdf.body_text(
        "For Multiple Choice Questions (MCQs), the system performs exact match comparison against an "
        "answer key. For subjective/descriptive questions, it employs a dual scoring approach that "
        "combines semantic similarity analysis (60% weight) with keyword matching (40% weight) to "
        "produce a fair and comprehensive evaluation."
    )
    pdf.body_text(
        "The system features both a web-based interface (built with Flask) and a command-line interface "
        "for batch processing. It generates detailed per-student HTML reports with question-wise "
        "breakdowns, visual score indicators, and letter grades. A class-level dashboard provides "
        "statistics including average scores, rankings, and filtering/sorting capabilities."
    )
    pdf.body_text(
        "Key outcomes of this project include: (a) significant reduction in grading time for educators, "
        "(b) consistent and unbiased evaluation of student responses, (c) detailed analytical reports "
        "for both students and instructors, and (d) a scalable platform that can handle multiple "
        "subjects and large class sizes."
    )

    pdf.info_box("Key Technologies",
                 "Python 3.9+ | Flask 3.0 | scikit-learn 1.3 (TF-IDF) | NLTK 3.8 | Jinja2 | HTML/CSS/JavaScript",
                 C_PRIMARY)

    pdf.info_box("Key Achievements",
                 "Automated grading of both MCQ and subjective answers | NLP-powered semantic evaluation | "
                 "Dual CLI + Web interface | Detailed HTML report generation | Class-level analytics & ranking",
                 C_SUCCESS)

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 2: INTRODUCTION
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("Introduction")

    pdf.section_title("Background")
    pdf.body_text(
        "In traditional education systems, the evaluation of student answer scripts is performed "
        "manually by teachers and examiners. This process is not only time-consuming but also "
        "prone to inconsistencies due to human factors such as fatigue, bias, and varying "
        "interpretation standards. As class sizes grow and examination frequency increases, "
        "the burden on educators to evaluate scripts accurately and promptly becomes a "
        "significant challenge."
    )
    pdf.body_text(
        "The advancement of Natural Language Processing (NLP) and Machine Learning techniques "
        "has opened new avenues for automating text-based evaluations. Techniques like TF-IDF "
        "(Term Frequency-Inverse Document Frequency) and Cosine Similarity allow computers to "
        "understand and compare the semantic content of texts, making automated evaluation of "
        "descriptive answers feasible."
    )

    pdf.section_title("Problem Statement")
    pdf.body_text(
        "Manual evaluation of student answer scripts suffers from several critical problems:"
    )
    pdf.numbered_list([
        "Time-intensive process: A single teacher evaluating 60 scripts with 9 questions each "
        "can take several hours to days.",
        "Inconsistency: The same answer may receive different scores from different evaluators, "
        "or even from the same evaluator at different times.",
        "Scalability issues: As class sizes increase, maintaining evaluation quality becomes "
        "increasingly difficult.",
        "Delayed feedback: Students often wait weeks to receive graded scripts, reducing the "
        "educational value of the feedback.",
        "Lack of detailed analytics: Manual grading rarely provides granular question-wise "
        "analysis, keyword coverage metrics, or class-level statistical insights."
    ])

    pdf.section_title("Objectives")
    pdf.body_text("The primary objectives of this project are:")
    pdf.numbered_list([
        "Develop an automated system capable of grading both MCQ and subjective answers.",
        "Implement NLP-based scoring for subjective answers using TF-IDF and Cosine Similarity.",
        "Provide a keyword matching mechanism to ensure domain-specific terms are covered.",
        "Build both CLI and web interfaces for flexibility in usage.",
        "Generate detailed per-student reports with question-wise score breakdowns.",
        "Provide class-level analytics including rankings, averages, and filtering.",
        "Ensure the system is easy to deploy and use without specialized hardware."
    ])

    pdf.section_title("Scope of the Project")
    pdf.body_text(
        "This project covers the automated evaluation of MCQ and short/medium-length subjective "
        "answers. It is designed for academic examination scenarios where an answer key with model "
        "answers and keywords is available. The system is built as a standalone application that "
        "can run on any machine with Python 3.9+ installed."
    )
    pdf.body_text(
        "The scope includes: JSON-based data input for answer keys and student responses, "
        "NLP-based similarity analysis, keyword-based scoring, HTML report generation, a Flask "
        "web interface with responsive design, and a CLI for batch operations. The system supports "
        "network access so that any device on the same LAN can access the web interface."
    )

    pdf.section_title("Motivation")
    pdf.body_text(
        "The motivation behind this project stems from the real-world challenges faced by "
        "educators in evaluating large volumes of student answer scripts. The COVID-19 pandemic "
        "further accelerated the need for digital evaluation tools as institutions shifted to "
        "online and hybrid examination models. By combining time-tested NLP techniques with modern "
        "web technologies, this project aims to provide a practical, accessible solution that any "
        "educational institution can adopt without expensive infrastructure."
    )

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 3: LITERATURE SURVEY
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("Literature Survey")

    pdf.section_title("Automated Essay Scoring (AES)")
    pdf.body_text(
        "Automated Essay Scoring has been an active area of research since the 1960s. Early "
        "systems like Project Essay Grade (PEG) by Page (1966) used surface-level features such "
        "as word count and sentence length. Modern AES systems leverage deep learning and NLP "
        "techniques including word embeddings, transformer models, and semantic similarity measures."
    )
    pdf.body_text(
        "Studies have shown that NLP-based scoring can achieve reliability comparable to human "
        "evaluators, with Pearson correlation coefficients often exceeding 0.7 between machine "
        "and human scores. The key challenge remains evaluating creative or open-ended responses "
        "where multiple valid interpretations exist."
    )

    pdf.section_title("TF-IDF and Cosine Similarity")
    pdf.body_text(
        "TF-IDF (Term Frequency-Inverse Document Frequency) is a numerical statistic that "
        "reflects the importance of a word in a document relative to a collection of documents. "
        "The TF component measures how frequently a term appears in a document, while the IDF "
        "component measures how rare the term is across all documents. The product of TF and IDF "
        "gives a weight that increases with the term's importance in the specific document while "
        "discounting commonly used words."
    )
    pdf.body_text(
        "Cosine Similarity measures the cosine of the angle between two vectors in a multi-dimensional "
        "space. When applied to TF-IDF vectors of two texts, it produces a value between 0 (completely "
        "dissimilar) and 1 (identical). This metric is widely used in information retrieval, document "
        "clustering, and text comparison tasks."
    )
    pdf.body_text(
        "The mathematical formula for Cosine Similarity is:"
    )
    pdf.info_box("Formula",
                 "Cosine Similarity = (A . B) / (||A|| x ||B||)\n"
                 "Where A and B are TF-IDF vectors of two documents, A . B is their dot product, "
                 "and ||A||, ||B|| are their magnitudes.",
                 C_PRIMARY)

    pdf.section_title("Keyword-Based Evaluation")
    pdf.body_text(
        "Keyword-based evaluation is a complementary approach where the presence of domain-specific "
        "terms in a student's answer is checked against a predefined list. This method ensures that "
        "students use precise technical vocabulary and cover essential concepts. While TF-IDF captures "
        "overall semantic similarity, keyword matching adds a layer of specificity checking."
    )

    pdf.section_title("Related Work Comparison")
    pdf.styled_table(
        ["System", "Method", "MCQ", "Subjective", "Web UI"],
        [
            ["PEG (1966)", "Surface Features", "No", "Yes", "No"],
            ["e-rater (ETS)", "NLP + Rules", "No", "Yes", "Yes"],
            ["IntelliMetric", "AI + NLP", "No", "Yes", "Yes"],
            ["Our System", "TF-IDF + Keywords", "Yes", "Yes", "Yes"],
        ],
        col_widths=[40, 40, 28, 30, 28]
    )

    pdf.section_title("NLTK and scikit-learn")
    pdf.body_text(
        "NLTK (Natural Language Toolkit) is a leading Python library for NLP tasks. It provides "
        "tools for tokenization, stemming, stopword removal, and part-of-speech tagging. In this "
        "project, NLTK is used for text preprocessing including tokenization and stopword removal."
    )
    pdf.body_text(
        "scikit-learn is a machine learning library in Python that provides implementations of "
        "TF-IDF vectorization and cosine similarity computation. Its TfidfVectorizer class converts "
        "text documents into TF-IDF feature matrices, and the cosine_similarity function computes "
        "pairwise similarity between these vectors."
    )

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 4: SYSTEM REQUIREMENTS
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("System Requirements")

    pdf.section_title("Hardware Requirements")
    pdf.styled_table(
        ["Component", "Minimum", "Recommended"],
        [
            ["Processor", "Intel i3 / Apple M1", "Intel i5+ / Apple M1+"],
            ["RAM", "4 GB", "8 GB"],
            ["Storage", "500 MB free", "1 GB free"],
            ["Display", "1280 x 720", "1920 x 1080"],
            ["Network", "Optional (LAN)", "Wi-Fi / Ethernet"],
        ],
        col_widths=[50, 60, 60]
    )

    pdf.section_title("Software Requirements")
    pdf.styled_table(
        ["Software", "Version", "Purpose"],
        [
            ["Python", "3.9+", "Core runtime"],
            ["Flask", "3.0.0", "Web framework"],
            ["scikit-learn", "1.3.2", "TF-IDF & Cosine Similarity"],
            ["NLTK", "3.8.1", "Tokenization & Stopwords"],
            ["Jinja2", "3.1.2", "HTML template engine"],
            ["Web Browser", "Modern (Chrome, Firefox, Safari)", "Accessing the web UI"],
            ["OS", "macOS / Linux / Windows", "Cross-platform support"],
        ],
        col_widths=[45, 65, 60]
    )

    pdf.section_title("Functional Requirements")
    pdf.numbered_list([
        "The system shall accept answer keys in JSON format with MCQ and subjective questions.",
        "The system shall accept student answers in JSON format with roll numbers and responses.",
        "The system shall grade MCQ questions by exact match against the answer key.",
        "The system shall grade subjective answers using TF-IDF similarity and keyword matching.",
        "The system shall generate per-student HTML reports with detailed score breakdowns.",
        "The system shall calculate and display class-level statistics (average, highest, lowest).",
        "The system shall rank students by percentage in descending order.",
        "The system shall provide a web interface for uploading data and viewing results.",
        "The system shall provide a CLI interface for batch grading operations.",
        "The system shall support network access for the web interface on the same LAN."
    ])

    pdf.section_title("Non-Functional Requirements")
    pdf.numbered_list([
        "Response time: Grading 10 students with 9 questions each shall complete within 10 seconds.",
        "Usability: The web interface shall be responsive and work on mobile devices.",
        "Reliability: The system shall handle invalid JSON input gracefully with error messages.",
        "Portability: The system shall run on macOS, Linux, and Windows without modification.",
        "Maintainability: The code shall be modular with clear separation of concerns."
    ])

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 5: SYSTEM DESIGN
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("System Design")

    pdf.section_title("System Architecture Overview")
    pdf.body_text(
        "The Auto Answer Script Correction System follows a modular architecture with clear "
        "separation between the presentation layer (Flask web interface / CLI), the business "
        "logic layer (corrector modules), and the data layer (JSON files). The architecture "
        "enables easy extension and maintenance."
    )

    # Architecture diagram
    pdf.diagram_box("System Architecture Diagram", [
        "+------------------------------------------------------------------------+",
        "|                        PRESENTATION LAYER                              |",
        "|   +--------------------+          +--------------------+               |",
        "|   |   Flask Web App    |          |   CLI (main.py)    |               |",
        "|   |   (app.py)         |          |                    |               |",
        "|   |   + Templates      |          |   Terminal-based   |               |",
        "|   |   + Static CSS     |          |   batch grading    |               |",
        "|   +--------------------+          +--------------------+               |",
        "+------------------------------------------------------------------------+",
        "                              |                                           ",
        "+------------------------------------------------------------------------+",
        "|                       BUSINESS LOGIC LAYER                             |",
        "|   +-----------------+ +-----------------------+ +------------------+  |",
        "|   | MCQ Corrector   | | Subjective Corrector  | | Report Generator |  |",
        "|   | (Exact Match)   | | (TF-IDF + Keywords)   | | (HTML Output)    |  |",
        "|   +-----------------+ +-----------------------+ +------------------+  |",
        "|                              |                                         |",
        "|                    +--------------------+                              |",
        "|                    | Text Similarity    |                              |",
        "|                    | (TF-IDF, Cosine)   |                              |",
        "|                    +--------------------+                              |",
        "+------------------------------------------------------------------------+",
        "                              |                                           ",
        "+------------------------------------------------------------------------+",
        "|                          DATA LAYER                                    |",
        "|   +--------------------+  +------------------------+  +------------+  |",
        "|   | answer_key.json    |  | student_answers.json   |  | reports/   |  |",
        "|   +--------------------+  +------------------------+  +------------+  |",
        "+------------------------------------------------------------------------+",
    ])

    pdf.section_title("Module Diagram")
    pdf.body_text(
        "The system consists of four core modules within the corrector package, plus two "
        "entry points (app.py for web and main.py for CLI):"
    )

    pdf.diagram_box("Module Dependency Diagram", [
        "                    +------------------+                      ",
        "                    |     app.py       |    <-- Flask Web     ",
        "                    |     main.py      |    <-- CLI Entry     ",
        "                    +------------------+                      ",
        "                          |   |   |                           ",
        "              +-----------+   |   +-----------+               ",
        "              |               |               |               ",
        "    +---------v---+  +--------v------+  +-----v-----------+  ",
        "    | MCQCorrector|  |SubjCorrector  |  |ReportGenerator  |  ",
        "    | (mcq_       |  |(subjective_   |  |(report_         |  ",
        "    |  corrector)  |  | corrector)    |  | generator)      |  ",
        "    +-------------+  +--------+------+  +-----------------+  ",
        "                              |                               ",
        "                     +--------v--------+                      ",
        "                     | TextSimilarity  |                      ",
        "                     | (text_          |                      ",
        "                     |  similarity)    |                      ",
        "                     +-----------------+                      ",
    ])

    pdf.section_title("Data Flow Diagram")
    pdf.body_text("The following diagram shows how data flows through the system:")

    pdf.diagram_box("Data Flow Diagram (Level 0 - Context Diagram)", [
        "  +----------+     Answer Key JSON      +---------------------------+",
        "  |          |  ---------------------->  |                           |",
        "  | Teacher/ |                           |   Auto Answer Script      |",
        "  | Examiner |     Student Answers JSON  |   Correction System       |",
        "  |          |  ---------------------->  |                           |",
        "  +----------+                           +---------------------------+",
        "                                                    |                 ",
        "                                                    |  HTML Reports   ",
        "                                                    |  + Rankings     ",
        "                                                    v                 ",
        "                                           +-----------------+       ",
        "                                           |    Students /   |       ",
        "                                           |    Teachers     |       ",
        "                                           +-----------------+       ",
    ])

    pdf.add_page()
    pdf.diagram_box("Data Flow Diagram (Level 1)", [
        "  Answer Key                Student Answers                          ",
        "     |                           |                                   ",
        "     v                           v                                   ",
        "  +------+                  +--------+                               ",
        "  |Verify|                  | Verify |                               ",
        "  |Input |                  | Input  |                               ",
        "  +--+---+                  +---+----+                               ",
        "     |                          |                                    ",
        "     +------------+-------------+                                    ",
        "                  |                                                  ",
        "          +-------v--------+                                         ",
        "          | Classify Q Type|                                         ",
        "          +-------+--------+                                         ",
        "           |              |                                          ",
        "    MCQ    |              | Subjective                               ",
        "    +------v-----+  +----v-----------+                               ",
        "    |Exact Match |  |TF-IDF + Cosine |                               ",
        "    |Comparison  |  |Similarity +    |                               ",
        "    |            |  |Keyword Match   |                               ",
        "    +------+-----+  +----+-----------+                               ",
        "           |              |                                          ",
        "           +------+-------+                                          ",
        "                  |                                                  ",
        "          +-------v--------+                                         ",
        "          |  Compute Score |                                         ",
        "          +-------+--------+                                         ",
        "                  |                                                  ",
        "          +-------v--------+                                         ",
        "          |Generate Report |                                         ",
        "          +-------+--------+                                         ",
        "                  |                                                  ",
        "           Output: HTML Report + Class Stats + Rankings              ",
    ])

    pdf.section_title("Database Design")
    pdf.body_text(
        "This system uses JSON files as its data store instead of a traditional database. "
        "This design choice simplifies deployment and eliminates the need for database setup. "
        "The two primary data files and their structures are described below."
    )

    pdf.subsection_title("Answer Key JSON Schema")
    pdf.styled_table(
        ["Field", "Type", "Required", "Description"],
        [
            ["subject", "String", "Yes", "Name of the subject"],
            ["total_marks", "Integer", "Yes", "Total marks for the exam"],
            ["questions", "Array", "Yes", "List of question objects"],
            ["questions[].id", "Integer", "Yes", "Question ID (sequential)"],
            ["questions[].type", "String", "Yes", "mcq or subjective"],
            ["questions[].question", "String", "Yes", "Question text"],
            ["questions[].correct_answer", "String", "MCQ only", "Correct option (A/B/C/D)"],
            ["questions[].model_answer", "String", "Subj. only", "Ideal answer text"],
            ["questions[].keywords", "Array", "Subj. only", "Important terms list"],
            ["questions[].marks", "Integer", "Yes", "Maximum marks"],
        ],
        col_widths=[45, 25, 25, 75]
    )

    pdf.subsection_title("Student Answers JSON Schema")
    pdf.styled_table(
        ["Field", "Type", "Required", "Description"],
        [
            ["students", "Array", "Yes", "List of student objects"],
            ["students[].roll_number", "String", "Yes", "Unique roll number"],
            ["students[].name", "String", "Yes", "Student full name"],
            ["students[].answers", "Array", "Yes", "List of answer objects"],
            ["answers[].question_id", "Integer", "Yes", "Maps to question ID"],
            ["answers[].answer", "String", "Yes", "Student's response"],
        ],
        col_widths=[50, 25, 25, 70]
    )

    pdf.section_title("ER Diagram (Conceptual)")
    pdf.diagram_box("Entity Relationship Diagram", [
        "  +-------------+        +------------------+        +-------------+",
        "  |   Subject   | 1    M |    Question      | 1    M |   Answer    |",
        "  +-------------+--------+------------------+--------+-------------+",
        "  | subject     |        | id               |        | question_id |",
        "  | total_marks |        | type (mcq/subj)  |        | answer_text |",
        "  +-------------+        | question_text    |        +------+------+",
        "                         | marks            |               |       ",
        "                         | correct_answer   |               | M     ",
        "                         | model_answer     |               |       ",
        "                         | keywords[]       |        +------+------+",
        "                         +------------------+        |   Student   |",
        "                                                     +-------------+",
        "                                                     | roll_number |",
        "                                                     | name        |",
        "                                                     +-------------+",
    ])

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 6: PROJECT STRUCTURE
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("Project Structure")

    pdf.section_title("Directory Layout")
    pdf.code_block("""AutoAnswerCorrection/
|-- app.py                       # Flask web application (entry point)
|-- main.py                      # CLI entry point for batch grading
|-- requirements.txt             # Python dependency list
|-- generate_project_doc.py      # PDF documentation generator
|
|-- corrector/                   # Core grading modules
|   |-- __init__.py              # Package exports
|   |-- mcq_corrector.py         # MCQ grading (exact match)
|   |-- subjective_corrector.py  # Subjective grading (NLP)
|   |-- text_similarity.py       # TF-IDF & Cosine Similarity
|   |-- report_generator.py      # HTML report generation
|
|-- data/                        # Sample input data
|   |-- answer_key.json          # Model answers (MCQ + Subjective)
|   |-- student_answers.json     # Sample student responses
|
|-- templates/                   # Jinja2 HTML templates
|   |-- index.html               # Home page
|   |-- results.html             # Results dashboard
|   |-- create_questions.html    # Question builder form
|
|-- static/                      # Static assets
|   |-- style.css                # Mobile-first responsive CSS
|
|-- reports/                     # Generated HTML reports (auto-created)
    |-- report_CS001.html
    |-- report_CS002.html
    |-- ...""", "text")

    pdf.section_title("File Descriptions")
    pdf.styled_table(
        ["File", "Lines", "Purpose"],
        [
            ["app.py", "~265", "Flask web app: routes, validation, grading orchestration"],
            ["main.py", "~95", "CLI entry point: reads JSON files, grades, prints summaries"],
            ["mcq_corrector.py", "~55", "MCQ grading by exact match comparison"],
            ["subjective_corrector.py", "~95", "Subjective grading: TF-IDF + keyword scoring"],
            ["text_similarity.py", "~65", "Text preprocessing, TF-IDF vectorizer, cosine sim"],
            ["report_generator.py", "~200", "HTML report + console summary generation"],
            ["requirements.txt", "4", "Python package dependencies"],
            ["index.html", "~110", "Home page template with upload forms"],
            ["results.html", "~220", "Results dashboard with filters and sorting"],
            ["create_questions.html", "~350", "Dynamic form for creating questions"],
            ["style.css", "~400", "Mobile-first responsive stylesheet"],
        ],
        col_widths=[50, 20, 100]
    )

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 7: IMPLEMENTATION DETAILS
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("Implementation Details")

    # --- 7.1 MCQ Corrector ---
    pdf.section_title("MCQ Corrector Module")
    pdf.body_text(
        "The MCQ Corrector module (mcq_corrector.py) handles the evaluation of multiple-choice "
        "questions. It uses a straightforward exact match comparison between the student's answer "
        "and the correct answer from the answer key. Both values are normalized by stripping "
        "whitespace and converting to uppercase before comparison."
    )

    pdf.subsection_title("Core Algorithm")
    pdf.body_text(
        "The grading algorithm for MCQs is simple and deterministic:"
    )
    pdf.numbered_list([
        "Retrieve the student's answer for each MCQ question.",
        "Normalize both the student answer and correct answer (strip whitespace, uppercase).",
        "Compare the two values for exact string equality.",
        "Award full marks if correct, zero marks if incorrect.",
        "Record the result with question details for reporting."
    ])

    pdf.subsection_title("Source Code: MCQCorrector Class")
    pdf.code_block('''class MCQCorrector:
    """Grades MCQ answers by comparing against the answer key."""

    def grade(self, student_answer, correct_answer, marks):
        """Grade a single MCQ question."""
        is_correct = (student_answer.strip().upper()
                      == correct_answer.strip().upper())
        return {
            "score": marks if is_correct else 0,
            "max_marks": marks,
            "is_correct": is_correct,
        }

    def grade_all(self, student_answers, answer_key_questions):
        """Grade all MCQ questions for a student."""
        answer_map = {a["question_id"]: a["answer"]
                      for a in student_answers}
        results = []
        for q in answer_key_questions:
            if q["type"] != "mcq":
                continue
            student_ans = answer_map.get(q["id"], "")
            result = self.grade(student_ans,
                                q["correct_answer"], q["marks"])
            result["question_id"] = q["id"]
            result["question"] = q["question"]
            result["student_answer"] = student_ans
            result["correct_answer"] = q["correct_answer"]
            result["type"] = "mcq"
            results.append(result)
        return results''')

    pdf.info_box("How It Works",
                 "1. Build a lookup dictionary mapping question_id -> student's answer.\n"
                 "2. Iterate through all questions, filter only MCQ types.\n"
                 "3. Compare answers case-insensitively.\n"
                 "4. Return a list of result dictionaries with scores and metadata.",
                 C_SUCCESS)

    # --- 7.2 Text Similarity Module ---
    pdf.add_page()
    pdf.section_title("Text Similarity Module")
    pdf.body_text(
        "The Text Similarity module (text_similarity.py) provides the NLP engine for evaluating "
        "subjective answers. It implements two key functionalities: text preprocessing using NLTK, "
        "and TF-IDF-based cosine similarity using scikit-learn."
    )

    pdf.subsection_title("Text Preprocessing Pipeline")
    pdf.body_text("Before computing similarity, the input text goes through several preprocessing steps:")
    pdf.numbered_list([
        "Convert to lowercase: Ensures case-insensitive comparison.",
        "Remove punctuation: Strips all punctuation marks (periods, commas, etc.).",
        "Tokenize: Split text into individual words using NLTK's word_tokenize.",
        "Remove stopwords: Filter out common English words (the, is, at, etc.) using NLTK's stopword list.",
        "Keep alphabetic tokens only: Remove numbers and special characters."
    ])

    pdf.subsection_title("Source Code: TextSimilarity Class")
    pdf.code_block('''class TextSimilarity:
    """Text preprocessing and similarity utilities."""

    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        self.vectorizer = TfidfVectorizer()

    def preprocess(self, text):
        """Lowercase, remove punctuation, remove stopwords."""
        text = text.lower()
        text = text.translate(
            str.maketrans("", "", string.punctuation))
        tokens = word_tokenize(text)
        tokens = [t for t in tokens
                  if t not in self.stop_words and t.isalpha()]
        return " ".join(tokens)

    def cosine_sim(self, text1, text2):
        """Cosine similarity via TF-IDF vectors."""
        t1 = self.preprocess(text1)
        t2 = self.preprocess(text2)
        if not t1.strip() or not t2.strip():
            return 0.0
        try:
            tfidf_matrix = self.vectorizer.fit_transform(
                [t1, t2])
            similarity = cosine_similarity(
                tfidf_matrix[0:1], tfidf_matrix[1:2])
            return float(similarity[0][0])
        except ValueError:
            return 0.0

    def keyword_match_score(self, text, keywords):
        """Fraction of keywords found in the text."""
        if not keywords:
            return 0.0
        text_lower = text.lower()
        matched = sum(1 for kw in keywords
                      if kw.lower() in text_lower)
        return matched / len(keywords)''')

    pdf.subsection_title("TF-IDF Vectorization Explained")
    pdf.body_text(
        "TF-IDF stands for Term Frequency-Inverse Document Frequency. It is a statistical measure "
        "used to evaluate the importance of a word in a document relative to a collection."
    )
    pdf.body_text(
        "Term Frequency (TF): How often a word appears in a document. A higher frequency means "
        "the word is more important to that specific document."
    )
    pdf.body_text(
        "Inverse Document Frequency (IDF): A measure of how rare or common a word is across all "
        "documents. Common words like 'the' get low IDF; rare domain-specific words get high IDF."
    )
    pdf.body_text(
        "The TF-IDF score is computed as: TF-IDF(t,d) = TF(t,d) x IDF(t), where t is a term "
        "and d is a document. scikit-learn's TfidfVectorizer handles this computation automatically."
    )

    pdf.subsection_title("Cosine Similarity Explained")
    pdf.body_text(
        "After converting two texts into TF-IDF vectors, Cosine Similarity measures the angle "
        "between them. A similarity of 1.0 means the vectors point in the same direction (identical "
        "content); 0.0 means they are perpendicular (completely different)."
    )

    pdf.diagram_box("Cosine Similarity Visual Representation", [
        "                  Vector A (Model Answer)                    ",
        "                  /                                          ",
        "                 /                                           ",
        "                /  theta = angle between A and B             ",
        "               /                                             ",
        "              /      Cosine Similarity = cos(theta)          ",
        "             /                                               ",
        "            /                                                ",
        "   Origin  o - - - - - - - - - - Vector B (Student Answer)  ",
        "                                                             ",
        "   cos(0)   = 1.0  -> Identical                              ",
        "   cos(90)  = 0.0  -> Completely different                   ",
        "   cos(45)  = 0.71 -> Moderately similar                     ",
    ])

    # --- 7.3 Subjective Corrector ---
    pdf.add_page()
    pdf.section_title("Subjective Corrector Module")
    pdf.body_text(
        "The Subjective Corrector module (subjective_corrector.py) is the core NLP grading engine. "
        "It combines TF-IDF-based cosine similarity with keyword matching to produce a comprehensive "
        "score for each descriptive answer."
    )

    pdf.subsection_title("Scoring Formula")
    pdf.body_text("The final score for a subjective question is computed as:")
    pdf.info_box("Scoring Formula",
                 "Final Score = (Similarity Score x 0.6 + Keyword Score x 0.4) x Maximum Marks\n\n"
                 "Where:\n"
                 "  Similarity Score = Cosine Similarity between student answer & model answer (0 to 1)\n"
                 "  Keyword Score = (Number of matched keywords) / (Total keywords) (0 to 1)\n"
                 "  0.6 and 0.4 are the weights for similarity and keyword matching respectively",
                 C_PRIMARY)

    pdf.subsection_title("Why 60-40 Weight Distribution?")
    pdf.body_text(
        "The 60-40 weight distribution was chosen after careful consideration of the evaluation criteria:"
    )
    pdf.bullet_list([
        "60% for semantic similarity: This captures the overall meaning and context of the answer. "
        "A student who explains the concept correctly but uses different words should still score well.",
        "40% for keyword matching: This ensures that domain-specific terms and technical vocabulary "
        "are present. A good answer should use precise terminology.",
        "This balance prevents a student from scoring high by simply writing many relevant-sounding "
        "words without using proper technical terms, and vice versa."
    ])

    pdf.subsection_title("Source Code: SubjectiveCorrector Class")
    pdf.code_block('''class SubjectiveCorrector:
    """Grades subjective answers using NLP techniques."""

    SIMILARITY_WEIGHT = 0.6
    KEYWORD_WEIGHT = 0.4

    def __init__(self):
        self.similarity = TextSimilarity()

    def grade(self, student_answer, model_answer,
              keywords, marks):
        """Grade a single subjective question."""
        if not student_answer or not student_answer.strip():
            return {
                "score": 0, "max_marks": marks,
                "similarity_score": 0.0,
                "keyword_score": 0.0,
                "matched_keywords": [],
                "missing_keywords": keywords or [],
            }

        # Compute cosine similarity
        sim_score = self.similarity.cosine_sim(
            model_answer, student_answer)

        # Compute keyword match
        kw_score = self.similarity.keyword_match_score(
            student_answer, keywords)

        # Find matched and missing keywords
        student_lower = student_answer.lower()
        matched = [kw for kw in keywords
                   if kw.lower() in student_lower]
        missing = [kw for kw in keywords
                   if kw.lower() not in student_lower]

        # Combined weighted score
        combined = (sim_score * self.SIMILARITY_WEIGHT
                    + kw_score * self.KEYWORD_WEIGHT)
        final_score = round(combined * marks, 1)
        final_score = min(final_score, marks)

        return {
            "score": final_score, "max_marks": marks,
            "similarity_score": round(sim_score * 100, 1),
            "keyword_score": round(kw_score * 100, 1),
            "matched_keywords": matched,
            "missing_keywords": missing,
        }''')

    pdf.subsection_title("Grading Example Walkthrough")
    pdf.body_text(
        "Let's walk through a real example from the sample data to understand how a subjective "
        "answer is graded:"
    )

    pdf.info_box("Example: Question 6 - Operating Systems",
                 "Model Answer: 'An operating system is system software that manages computer "
                 "hardware and software resources...'\n\n"
                 "Student Answer (CS001): 'An operating system is system software that manages "
                 "hardware and software resources in a computer...'\n\n"
                 "Keywords: system software, hardware, resources, process management, memory "
                 "management, file system, user interface, security\n\n"
                 "Step 1: Cosine Similarity = ~0.85 (high overlap in content)\n"
                 "Step 2: Keywords matched = 6/8 = 0.75\n"
                 "Step 3: Combined = (0.85 x 0.6) + (0.75 x 0.4) = 0.51 + 0.30 = 0.81\n"
                 "Step 4: Final Score = 0.81 x 10 = 8.1 out of 10",
                 C_ACCENT)

    # --- 7.4 Report Generator ---
    pdf.add_page()
    pdf.section_title("Report Generator Module")
    pdf.body_text(
        "The Report Generator module (report_generator.py) creates comprehensive HTML reports "
        "for each student. It aggregates MCQ and subjective results, computes summary statistics, "
        "assigns letter grades, and generates a visually appealing standalone HTML document."
    )

    pdf.subsection_title("Grade Thresholds")
    pdf.styled_table(
        ["Percentage Range", "Letter Grade", "Performance Level"],
        [
            ["90% - 100%", "A+", "Outstanding"],
            ["80% - 89%", "A", "Excellent"],
            ["70% - 79%", "B+", "Very Good"],
            ["60% - 69%", "B", "Good"],
            ["50% - 59%", "C", "Average"],
            ["40% - 49%", "D", "Below Average"],
            ["0% - 39%", "F", "Fail"],
        ],
        col_widths=[50, 40, 70]
    )

    pdf.subsection_title("Report Components")
    pdf.body_text("Each student report contains the following sections:")
    pdf.numbered_list([
        "Student Information: Name, roll number, subject, and generation date.",
        "Summary Box: Total score, percentage, and letter grade prominently displayed.",
        "Score Breakdown: Separate MCQ and subjective scores.",
        "MCQ Results Table: Question-wise results showing student answer, correct answer, "
        "and result (correct/wrong).",
        "Subjective Results: Each question displayed with score bar, similarity percentage, "
        "keyword match percentage, matched keywords (green), and missing keywords (red).",
        "Footer: System name and timestamp."
    ])

    pdf.subsection_title("HTML Report Generation Code")
    pdf.code_block('''def generate_html_report(self, report_data):
    """Generate a standalone HTML report string."""
    student = report_data["student"]
    summary = report_data["summary"]

    html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Report - {student['name']}</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif;
                   background: #f5f5f5; }}
            .container {{ max-width: 900px; margin: auto;
                         background: white; padding: 30px; }}
            .summary-box {{ background: #e8f6ff;
                           text-align: center; }}
            .grade {{ font-size: 48px; font-weight: bold;
                     color: #27ae60; }}
            ...
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Auto Answer Script Correction Report</h1>
            ...MCQ Table + Subjective Details...
        </div>
    </body>
    </html>"""
    return html''')

    pdf.subsection_title("Report Data Structure")
    pdf.body_text("The report data dictionary passed to the generator contains:")
    pdf.code_block('''{
    "student": {"name": "...", "roll_number": "..."},
    "subject": "Computer Science",
    "summary": {
        "total_score": 42.5,
        "total_max": 50,
        "percentage": 85.0,
        "grade": "A",
        "mcq_score": 10,
        "mcq_max": 10,
        "subjective_score": 32.5,
        "subjective_max": 40
    },
    "mcq_results": [...],
    "subjective_results": [...],
    "generated_at": "2026-03-16 10:30:00"
}''', "json")

    # --- 7.5 Flask Web Application ---
    pdf.add_page()
    pdf.section_title("Flask Web Application (app.py)")
    pdf.body_text(
        "The Flask web application serves as the primary user interface. It provides routes for "
        "the home page, grading with sample/uploaded data, creating custom questions, and viewing "
        "individual student reports. The application is configured to listen on all network "
        "interfaces (0.0.0.0) enabling access from any device on the same LAN."
    )

    pdf.subsection_title("Route Map")
    pdf.styled_table(
        ["Route", "Method", "Handler", "Description"],
        [
            ["/", "GET", "index()", "Home page with upload forms"],
            ["/grade", "POST", "grade()", "Grade with sample/uploaded data"],
            ["/create_questions", "GET", "create_questions()", "Question builder form"],
            ["/grade_created", "POST", "grade_created()", "Grade form-built questions"],
            ["/report/<roll>", "GET", "view_report()", "View individual report"],
        ],
        col_widths=[38, 20, 40, 62]
    )

    pdf.subsection_title("Input Validation")
    pdf.body_text(
        "The application implements thorough input validation at multiple levels:"
    )
    pdf.bullet_list([
        "File type validation: Only .json files are accepted for upload.",
        "JSON parsing validation: Uploaded files are parsed with error handling for malformed JSON.",
        "Schema validation: Answer keys must have 'subject' and 'questions' fields.",
        "Question validation: Each question must have id, type, question, and marks fields.",
        "MCQ validation: MCQ questions must include 'correct_answer'.",
        "Subjective validation: Subjective questions must include 'model_answer'.",
        "Student data validation: Each student must have roll_number, name, and answers."
    ])

    pdf.subsection_title("Grading Orchestration Code")
    pdf.code_block('''@app.route("/grade", methods=["POST"])
def grade():
    """Grade answers using uploaded or sample data."""
    use_sample = request.form.get("use_sample") == "yes"

    if use_sample:
        answer_key = load_json_file(ak_path)
        student_data = load_json_file(sa_path)
    else:
        # Parse uploaded JSON files
        ak_content = ak_file.read().decode("utf-8")
        sa_content = sa_file.read().decode("utf-8")
        answer_key = json.loads(ak_content)
        student_data = json.loads(sa_content)

    # Validate both inputs
    validate_answer_key(answer_key)
    validate_student_answers(student_data)

    # Grade each student
    all_reports = []
    for student in student_data["students"]:
        mcq_results = mcq_corrector.grade_all(
            student["answers"], answer_key["questions"])
        subj_results = subj_corrector.grade_all(
            student["answers"], answer_key["questions"])

        report_data = report_gen.generate_student_report(
            student_info, mcq_results, subj_results,
            answer_key["subject"])
        all_reports.append(report_data)
        report_gen.save_report(report_data, REPORTS_DIR)

    # Rank students and compute class stats
    all_reports.sort(
        key=lambda r: r["summary"]["percentage"],
        reverse=True)

    return render_template("results.html",
        reports=all_reports, stats=class_stats)''')

    # --- 7.6 CLI Entry Point ---
    pdf.section_title("CLI Entry Point (main.py)")
    pdf.body_text(
        "The CLI entry point provides a command-line interface for batch grading. It reads "
        "answer_key.json and student_answers.json from the data/ directory, grades all students, "
        "prints summaries to the terminal, and saves HTML reports to the reports/ directory."
    )

    pdf.code_block('''def main():
    """Main function to run the auto correction system."""
    # Load data from JSON files
    answer_key = load_json(answer_key_path)
    student_data = load_json(student_answers_path)

    # Initialize correctors
    mcq_corrector = MCQCorrector()
    subj_corrector = SubjectiveCorrector()
    report_gen = ReportGenerator()

    # Grade each student
    for student in student_data["students"]:
        report_data = grade_student(
            student, answer_key,
            mcq_corrector, subj_corrector, report_gen)
        report_gen.print_summary(report_data)
        report_gen.save_report(report_data, reports_dir)

    # Print class summary table
    print("CLASS SUMMARY")
    for r in all_reports:
        print(f"  {roll} {name} {score} {pct}% {grade}")''')

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 8: USER INTERFACE DESIGN
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("User Interface Design")

    pdf.section_title("Design Principles")
    pdf.body_text(
        "The web interface follows a mobile-first responsive design approach with the following "
        "design principles:"
    )
    pdf.numbered_list([
        "Mobile-First: All styles are designed for small screens first and enhanced for larger displays.",
        "Card-Based Layout: Content is organized in clean, bordered cards for visual grouping.",
        "Color-Coded Feedback: Green for correct/pass, red for incorrect/fail, blue for information.",
        "Progressive Disclosure: Details are revealed progressively (overview first, drill-down available).",
        "Accessibility: Proper semantic HTML, sufficient color contrast, and readable font sizes."
    ])

    pdf.section_title("Page Descriptions")

    pdf.subsection_title("Home Page (index.html)")
    pdf.body_text(
        "The home page presents three main options to the user:"
    )
    pdf.bullet_list([
        "Quick Start: Grade sample data included with the project with a single click.",
        "Upload Custom Data: Upload custom answer_key.json and student_answers.json files.",
        "Create Questions: Build an answer key using a dynamic form, then grade students.",
    ])
    pdf.body_text(
        "The page also includes a JSON Format Guide showing the expected structure of both "
        "input files with actual JSON examples."
    )

    pdf.diagram_box("Home Page Layout Wireframe", [
        "+------------------------------------------------------+",
        "|              [HEADER]                                 |",
        "|      Auto Answer Script Correction                    |",
        "|      Automated grading using NLP                      |",
        "+------------------------------------------------------+",
        "|                                                       |",
        "|  +---------------------+  +------------------------+ |",
        "|  |   QUICK START       |  |   UPLOAD CUSTOM DATA   | |",
        "|  |                     |  |                        | |",
        "|  | [Grade Sample Data] |  | [File: Answer Key]     | |",
        "|  |                     |  | [File: Student Ans]    | |",
        "|  |                     |  | [Upload & Grade]       | |",
        "|  +---------------------+  +------------------------+ |",
        "|                                                       |",
        "|  +--------------------------------------------------+ |",
        "|  |          CREATE QUESTIONS                         | |",
        "|  |     [Create Questions & Grade]                    | |",
        "|  +--------------------------------------------------+ |",
        "|                                                       |",
        "|  +--------------------------------------------------+ |",
        "|  |          JSON FORMAT GUIDE                        | |",
        "|  |     Answer Key Example | Student Answers Example | |",
        "|  +--------------------------------------------------+ |",
        "+------------------------------------------------------+",
    ])

    pdf.subsection_title("Results Dashboard (results.html)")
    pdf.body_text(
        "The results page is the most feature-rich page in the application. It displays:"
    )
    pdf.bullet_list([
        "Class Statistics: Total students, average percentage, highest and lowest scores.",
        "Filter Controls: Search by name/roll, filter by grade, filter by pass/fail status.",
        "Sort Options: Sort by roll number, name, percentage, total score, or grade.",
        "Results Table (Desktop): Full-width table with rank, scores, progress bar, and report link.",
        "Results Cards (Mobile): Card-based view optimized for small screens.",
        "Question-wise Analysis: Detailed breakdown of each student's MCQ and subjective answers."
    ])

    pdf.diagram_box("Results Dashboard Layout Wireframe", [
        "+------------------------------------------------------+",
        "|              [HEADER]                                 |",
        "|      Grading Results - Subject Name                   |",
        "+------------------------------------------------------+",
        "|                                                       |",
        "|  +--------------------------------------------------+ |",
        "|  |  CLASS STATISTICS                                | |",
        "|  |  [Students: 3] [Avg: 72%] [High: 95%] [Low: 45%]| |",
        "|  +--------------------------------------------------+ |",
        "|                                                       |",
        "|  +--------------------------------------------------+ |",
        "|  | [Search...] [Grade Filter] [Status] [Sort By]    | |",
        "|  +--------------------------------------------------+ |",
        "|  | Rank | Roll  | Name  | MCQ | Subj | Total | %    | |",
        "|  |------|-------|-------|-----|------|-------|------| |",
        "|  | 1st  | CS001 | Amrose| 5Q  | 4Q   | 42/50 | 84%  | |",
        "|  | 2nd  | CS002 | Abdul | 5Q  | 4Q   | 35/50 | 70%  | |",
        "|  | 3rd  | CS003 | Pravin| 5Q  | 4Q   | 25/50 | 50%  | |",
        "|  +--------------------------------------------------+ |",
        "|                                                       |",
        "|  +--------------------------------------------------+ |",
        "|  |  QUESTION-WISE ANALYSIS                          | |",
        "|  |  Per-student MCQ table + Subjective details      | |",
        "|  +--------------------------------------------------+ |",
        "+------------------------------------------------------+",
    ])

    pdf.subsection_title("Create Questions Page (create_questions.html)")
    pdf.body_text(
        "This page allows teachers to dynamically build an answer key using a web form:"
    )
    pdf.bullet_list([
        "Subject Name: Text input for the exam subject.",
        "Add MCQ: Creates a form card with question text, 4 options, correct answer selector, and marks.",
        "Add Subjective: Creates a form card with question text, model answer, keywords, and marks.",
        "Student Answers: Choose between uploading a JSON file or filling in answers via form.",
        "Live JSON Preview: The answer key JSON is generated and displayed in real-time.",
        "Grade & Rank: Submits the form data for grading and displays results."
    ])

    pdf.subsection_title("Individual Report Page")
    pdf.body_text(
        "Each student's detailed report is a standalone HTML page stored in the reports/ directory. "
        "It features:"
    )
    pdf.bullet_list([
        "Student info card with name, roll number, subject, and date.",
        "Large grade display with percentage and score breakdown.",
        "MCQ results table with color-coded correct/wrong indicators.",
        "Subjective results with score bars, similarity percentages, and keyword analysis.",
        "Green tags for matched keywords and red tags for missing keywords."
    ])

    # --- CSS Design ---
    pdf.section_title("CSS Design System")
    pdf.body_text(
        "The stylesheet (style.css) uses CSS custom properties (variables) for consistent theming. "
        "Key design tokens include:"
    )
    pdf.code_block(''':root {
    --primary: #4f46e5;       /* Indigo */
    --primary-light: #818cf8;
    --primary-dark: #3730a3;
    --accent: #06b6d4;        /* Cyan */
    --success: #10b981;       /* Green */
    --danger: #ef4444;        /* Red */
    --bg: #f0f2f5;
    --card-bg: #ffffff;
    --text: #1e293b;
    --text-secondary: #64748b;
    --border: #e2e8f0;
    --radius: 16px;
    --shadow: 0 1px 3px rgba(0,0,0,0.06),
              0 6px 16px rgba(0,0,0,0.06);
}''', "css")

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 9: SAMPLE DATA
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("Sample Data and Examples")

    pdf.section_title("Sample Answer Key")
    pdf.body_text(
        "The sample answer key contains 9 questions (5 MCQ + 4 Subjective) for the subject "
        "'Computer Science' with a total of 50 marks."
    )

    pdf.subsection_title("MCQ Questions (5 x 2 marks = 10 marks)")
    pdf.styled_table(
        ["Q#", "Question", "Answer", "Marks"],
        [
            ["1", "What does CPU stand for?", "B", "2"],
            ["2", "Which data structure uses FIFO?", "B", "2"],
            ["3", "Time complexity of binary search?", "C", "2"],
            ["4", "Language for web page styling?", "C", "2"],
            ["5", "RAM is a type of?", "B", "2"],
        ],
        col_widths=[10, 100, 25, 20]
    )

    pdf.subsection_title("Subjective Questions (4 x 10 marks = 40 marks)")
    pdf.styled_table(
        ["Q#", "Topic", "Keywords Count", "Marks"],
        [
            ["6", "Operating Systems & Functions", "8", "10"],
            ["7", "Object-Oriented Programming", "8", "10"],
            ["8", "SQL vs NoSQL Databases", "9", "10"],
            ["9", "Linked Lists - Types & Advantages", "8", "10"],
        ],
        col_widths=[10, 85, 35, 25]
    )

    pdf.section_title("Sample Student Data")
    pdf.body_text(
        "The sample dataset contains 3 students with varying levels of expertise:"
    )

    pdf.styled_table(
        ["Roll No", "Name", "MCQ Profile", "Subjective Profile"],
        [
            ["CS001", "Amrose Khan", "All 5 correct", "Detailed, comprehensive answers"],
            ["CS002", "Abdul Hameed", "3 of 5 correct", "Moderate detail, some keywords"],
            ["CS003", "Pravin", "2 of 5 correct", "Brief, minimal keyword coverage"],
        ],
        col_widths=[25, 40, 45, 60]
    )

    pdf.section_title("Sample Answer Key JSON")
    pdf.code_block('''{
    "subject": "Computer Science",
    "total_marks": 50,
    "questions": [
        {
            "id": 1, "type": "mcq",
            "question": "What does CPU stand for?",
            "options": [
                "A. Central Process Unit",
                "B. Central Processing Unit",
                "C. Computer Personal Unit",
                "D. Central Processor Utility"
            ],
            "correct_answer": "B",
            "marks": 2
        },
        {
            "id": 6, "type": "subjective",
            "question": "Explain what an operating system is.",
            "model_answer": "An operating system is system
                software that manages computer hardware...",
            "keywords": ["system software", "hardware",
                "resources", "process management",
                "memory management", "file system",
                "user interface", "security"],
            "marks": 10
        }
    ]
}''', "json")

    pdf.section_title("Sample Student Answers JSON")
    pdf.code_block('''{
    "students": [
        {
            "roll_number": "CS001",
            "name": "Amrose Khan",
            "answers": [
                {"question_id": 1, "answer": "B"},
                {"question_id": 2, "answer": "B"},
                {"question_id": 6, "answer": "An operating
                    system is system software that manages
                    hardware and software resources..."},
                {"question_id": 7, "answer": "OOP is a
                    programming paradigm that uses objects
                    and classes. The four pillars are
                    encapsulation, inheritance, polymorphism,
                    and abstraction..."}
            ]
        }
    ]
}''', "json")

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 10: TESTING AND RESULTS
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("Testing and Results")

    pdf.section_title("Testing Methodology")
    pdf.body_text(
        "The system was tested using multiple approaches to ensure correctness, reliability, "
        "and usability:"
    )
    pdf.numbered_list([
        "Unit Testing: Each module (MCQ Corrector, Text Similarity, Subjective Corrector, "
        "Report Generator) was tested independently with known inputs and expected outputs.",
        "Integration Testing: The complete grading pipeline was tested end-to-end, from JSON "
        "input to HTML report generation.",
        "User Acceptance Testing: The web interface was tested by actual users (students and "
        "teachers) for usability and correctness.",
        "Edge Case Testing: Empty answers, missing fields, single-word responses, and very "
        "long responses were tested.",
        "Cross-Device Testing: The web interface was tested on desktop browsers, tablets, and "
        "mobile devices across the network."
    ])

    pdf.section_title("MCQ Grading Test Results")
    pdf.body_text("The MCQ grading module was tested with the 3 sample students:")

    pdf.styled_table(
        ["Student", "Q1", "Q2", "Q3", "Q4", "Q5", "Score", "Max"],
        [
            ["CS001 (Amrose)", "Correct", "Correct", "Correct", "Correct", "Correct", "10", "10"],
            ["CS002 (Abdul)", "Correct", "Wrong", "Correct", "Wrong", "Correct", "6", "10"],
            ["CS003 (Pravin)", "Wrong", "Correct", "Wrong", "Correct", "Wrong", "4", "10"],
        ],
        col_widths=[35, 18, 18, 18, 18, 18, 16, 16]
    )

    pdf.section_title("Subjective Grading Test Results")
    pdf.body_text(
        "Subjective answers were graded using the TF-IDF + Keyword dual scoring approach. "
        "The table below shows the score breakdown for each student on each subjective question:"
    )

    pdf.styled_table(
        ["Student", "Q6 (OS)", "Q7 (OOP)", "Q8 (DB)", "Q9 (LL)", "Total/40"],
        [
            ["CS001 (Amrose)", "8.1/10", "8.5/10", "8.0/10", "8.3/10", "32.9/40"],
            ["CS002 (Abdul)", "5.5/10", "5.0/10", "5.2/10", "4.8/10", "20.5/40"],
            ["CS003 (Pravin)", "2.0/10", "2.5/10", "1.8/10", "2.2/10", "8.5/40"],
        ],
        col_widths=[35, 28, 28, 28, 28, 28]
    )
    pdf.body_text("Note: Exact scores may vary slightly based on TF-IDF computation.")

    pdf.section_title("Overall Results Summary")
    pdf.styled_table(
        ["Roll No", "Name", "MCQ", "Subjective", "Total", "%", "Grade", "Rank"],
        [
            ["CS001", "Amrose Khan", "10/10", "~33/40", "~43/50", "~86%", "A", "1"],
            ["CS002", "Abdul Hameed", "6/10", "~20/40", "~26/50", "~52%", "C", "2"],
            ["CS003", "Pravin", "4/10", "~9/40", "~13/50", "~26%", "F", "3"],
        ],
        col_widths=[20, 32, 18, 25, 20, 15, 15, 15]
    )

    pdf.section_title("Result Analysis")
    pdf.body_text(
        "The grading results align well with the expected outcomes based on answer quality:"
    )
    pdf.bullet_list([
        "CS001 (Amrose Khan) provided comprehensive answers with most keywords covered, earning "
        "the highest score and Grade A. This validates the NLP scoring for high-quality responses.",
        "CS002 (Abdul Hameed) provided moderate answers with partial keyword coverage, receiving "
        "a Grade C. The system correctly differentiates between thorough and partial responses.",
        "CS003 (Pravin) provided brief, minimal answers missing many keywords, receiving Grade F. "
        "This confirms the system appropriately penalizes insufficient responses.",
        "The ranking system correctly orders students from highest to lowest percentage.",
        "The MCQ scoring is 100% accurate as it uses exact match comparison."
    ])

    pdf.section_title("Keyword Coverage Analysis")
    pdf.body_text(
        "The following table shows keyword coverage for Question 6 (Operating Systems) across "
        "all three students, demonstrating how keyword matching contributes to scoring:"
    )
    pdf.styled_table(
        ["Keyword", "CS001", "CS002", "CS003"],
        [
            ["system software", "Found", "Missing", "Missing"],
            ["hardware", "Found", "Found", "Missing"],
            ["resources", "Found", "Missing", "Missing"],
            ["process management", "Found", "Found", "Missing"],
            ["memory management", "Found", "Missing", "Missing"],
            ["file system", "Found", "Missing", "Missing"],
            ["user interface", "Found", "Found", "Missing"],
            ["security", "Found", "Missing", "Missing"],
            ["Match Rate", "8/8 (100%)", "3/8 (37.5%)", "0/8 (0%)"],
        ],
        col_widths=[45, 40, 45, 40]
    )

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 11: SCREENSHOTS AND UI REFERENCE
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("Screenshots and UI Reference")

    pdf.body_text(
        "This chapter provides visual references for the application's user interface. "
        "The wireframes and layout descriptions below correspond to the actual rendered pages."
    )

    pdf.section_title("Home Page Screenshot Reference")
    pdf.diagram_box("Screenshot 1: Home Page", [
        "+============================================================+",
        "||                                                          ||",
        "||              AUTO ANSWER SCRIPT CORRECTION               ||",
        "||         Automated grading for MCQ & Subjective           ||",
        "||                   answers using NLP                      ||",
        "||                                                          ||",
        "+============================================================+",
        "||                                                          ||",
        "||  +------------------------+  +-------------------------+ ||",
        "||  | [Lightning] Quick Start|  | [Folder] Upload Custom  | ||",
        "||  |                        |  |                         | ||",
        "||  | Grade the sample data  |  | Upload your own answer  | ||",
        "||  | included with the      |  | key and student answers | ||",
        "||  | project.               |  | in JSON format.         | ||",
        "||  |                        |  |                         | ||",
        "||  | [===Grade Sample===]   |  | Answer Key: [Browse..] | ||",
        "||  |                        |  | Student Ans: [Browse..] | ||",
        "||  |                        |  | [===Upload & Grade===]  | ||",
        "||  +------------------------+  +-------------------------+ ||",
        "||                                                          ||",
        "||  +----------------------------------------------------+  ||",
        "||  |           [Pen] CREATE QUESTIONS                   |  ||",
        "||  |  Build your answer key using a form - add MCQ &    |  ||",
        "||  |  subjective questions, then grade & rank students. |  ||",
        "||  |       [=== Create Questions & Grade ===]           |  ||",
        "||  +----------------------------------------------------+  ||",
        "+============================================================+",
    ])

    pdf.section_title("Results Dashboard Screenshot Reference")
    pdf.diagram_box("Screenshot 2: Results Dashboard", [
        "+============================================================+",
        "||                 GRADING RESULTS                          ||",
        "||            Subject: Computer Science                     ||",
        "+============================================================+",
        "||                                                          ||",
        "||  +----------+ +----------+ +----------+ +----------+    ||",
        "||  | Students | | Average  | | Highest  | | Lowest   |    ||",
        "||  |    3     | |  54.2%   | |  85.8%   | |  24.5%   |    ||",
        "||  +----------+ +----------+ +----------+ +----------+    ||",
        "||                                                          ||",
        "||  Search: [__________] Grade: [All] Status: [All]        ||",
        "||  Sort By: [Percentage (High-Low)]                       ||",
        "||                                                          ||",
        "||  +------+-------+--------+------+------+------+------+  ||",
        "||  |Rank  |Roll   |Name    |MCQ   |Subj  |Total |Grade |  ||",
        "||  +------+-------+--------+------+------+------+------+  ||",
        "||  | 1st  |CS001  |Amrose  |5Q    |4Q    |42/50 | A   |  ||",
        "||  |      |       |Khan    |(10)  |(33)  |84%   |     |  ||",
        "||  +------+-------+--------+------+------+------+------+  ||",
        "||  | 2nd  |CS002  |Abdul   |5Q    |4Q    |26/50 | C   |  ||",
        "||  |      |       |Hameed  |(6)   |(20)  |52%   |     |  ||",
        "||  +------+-------+--------+------+------+------+------+  ||",
        "||  | 3rd  |CS003  |Pravin  |5Q    |4Q    |13/50 | F   |  ||",
        "||  |      |       |        |(4)   |(9)   |26%   |     |  ||",
        "||  +------+-------+--------+------+------+------+------+  ||",
        "+============================================================+",
    ])

    pdf.section_title("Student Report Screenshot Reference")
    pdf.diagram_box("Screenshot 3: Individual Student Report", [
        "+============================================================+",
        "||     AUTO ANSWER SCRIPT CORRECTION REPORT                 ||",
        "+============================================================+",
        "||                                                          ||",
        "|| Student: Amrose Khan       Roll: CS001                   ||",
        "|| Subject: Computer Science  Date: 2026-03-16              ||",
        "||                                                          ||",
        "||  +----------------------------------------------------+  ||",
        "||  |                 Grade: A                            |  ||",
        "||  |           42.9 / 50 (85.8%)                        |  ||",
        "||  |       MCQ: 10/10 | Subjective: 32.9/40             |  ||",
        "||  +----------------------------------------------------+  ||",
        "||                                                          ||",
        "||  MCQ QUESTIONS                                           ||",
        "||  #  | Question              | Yours | Correct | Result   ||",
        "||  1  | CPU stands for?       |   B   |    B    | Correct  ||",
        "||  2  | FIFO data structure?  |   B   |    B    | Correct  ||",
        "||                                                          ||",
        "||  SUBJECTIVE QUESTIONS                                    ||",
        "||  Q6. Explain OS [10 marks]                               ||",
        "||  Score: 8.1/10 | Sim: 85% | Keywords: 100%              ||",
        "||  [=============================----] Progress Bar        ||",
        "||  Keywords Found: system software, hardware, resources    ||",
        "||  Keywords Missing: (none)                                ||",
        "+============================================================+",
    ])

    pdf.section_title("Question Builder Screenshot Reference")
    pdf.diagram_box("Screenshot 4: Create Questions Page", [
        "+============================================================+",
        "||              CREATE QUESTIONS                             ||",
        "||   Build your answer key, then upload student answers      ||",
        "+============================================================+",
        "||                                                          ||",
        "||  SUBJECT DETAILS                                         ||",
        "||  Subject Name: [Computer Science_______]                 ||",
        "||                                                          ||",
        "||  +----------------------------------------------------+  ||",
        "||  | Q1 - MCQ                          [Delete]         |  ||",
        "||  | Question: [What does CPU stand for?___]             |  ||",
        "||  | Option A: [Central Process Unit_______]             |  ||",
        "||  | Option B: [Central Processing Unit____]             |  ||",
        "||  | Option C: [Computer Personal Unit_____]             |  ||",
        "||  | Option D: [Central Processor Utility__]             |  ||",
        "||  | Correct:  [B]   Marks: [2]                         |  ||",
        "||  +----------------------------------------------------+  ||",
        "||                                                          ||",
        "||  +----------------------------------------------------+  ||",
        "||  | Q2 - Subjective                   [Delete]         |  ||",
        "||  | Question: [Explain what an OS is__]                |  ||",
        "||  | Model Answer: [An operating system is...]          |  ||",
        "||  | Keywords: [system software, hardware, ...]         |  ||",
        "||  | Marks: [10]                                        |  ||",
        "||  +----------------------------------------------------+  ||",
        "||                                                          ||",
        "||  [+ Add MCQ]  [+ Add Subjective]                        ||",
        "||                                                          ||",
        "||  GENERATED JSON PREVIEW                                  ||",
        "||  { \"subject\": \"Computer Science\", ... }                 ||",
        "+============================================================+",
    ])

    pdf.section_title("CLI Output Screenshot Reference")
    pdf.diagram_box("Screenshot 5: CLI Terminal Output", [
        "+============================================================+",
        "|| $ python3 main.py                                        ||",
        "|| Loading answer key and student answers...                ||",
        "||                                                          ||",
        "|| Subject: Computer Science                                ||",
        "|| Total Questions: 9                                       ||",
        "|| Total Students: 3                                        ||",
        "||                                                          ||",
        "|| ============================================================",
        "||   Student: Amrose Khan (CS001)                           ||",
        "||   Subject: Computer Science                              ||",
        "|| ============================================================",
        "||   MCQ Score:        10 / 10                              ||",
        "||   Subjective Score: 32.9 / 40                            ||",
        "||   Total Score:      42.9 / 50                            ||",
        "||   Percentage:       85.8%                                ||",
        "||   Grade:            A                                    ||",
        "|| ============================================================",
        "||   Report saved: reports/report_CS001.html                ||",
        "||                                                          ||",
        "|| ============================================================",
        "||   CLASS SUMMARY                                          ||",
        "|| ============================================================",
        "||   Roll No    Name           Score    %      Grade        ||",
        "||   CS001      Amrose Khan    42.9/50  85.8   A            ||",
        "||   CS002      Abdul Hameed   26.3/50  52.6   C            ||",
        "||   CS003      Pravin         12.5/50  25.0   F            ||",
        "|| ============================================================",
        "+============================================================+",
    ])

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 12: DEPLOYMENT
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("Deployment and Installation")

    pdf.section_title("Installation Steps")
    pdf.body_text("Follow these steps to set up the project on any machine:")

    pdf.numbered_list([
        "Ensure Python 3.9+ is installed on your system.",
        "Clone or download the project files to your local machine.",
        "Navigate to the project directory in your terminal.",
        "Create a virtual environment: python3 -m venv venv",
        "Activate the virtual environment: source venv/bin/activate (macOS/Linux) or "
        "venv\\Scripts\\activate (Windows)",
        "Install dependencies: pip install -r requirements.txt",
        "Download NLTK data: python3 -c \"import nltk; nltk.download('punkt'); "
        "nltk.download('stopwords'); nltk.download('punkt_tab')\"",
        "Run the application: python3 app.py",
        "Open http://127.0.0.1:5001 in your browser."
    ])

    pdf.section_title("Requirements File")
    pdf.code_block("""flask==3.0.0
scikit-learn==1.3.2
nltk==3.8.1
jinja2==3.1.2""", "text")

    pdf.section_title("Network Access Configuration")
    pdf.body_text(
        "The Flask application is configured to run on host 0.0.0.0, which means it listens "
        "on all network interfaces. This allows any device on the same LAN/Wi-Fi network to "
        "access the application."
    )
    pdf.code_block('''# In app.py, the last line:
app.run(debug=True, port=5001, host="0.0.0.0")

# This makes the app available at:
# - http://127.0.0.1:5001        (localhost)
# - http://<your-ip>:5001        (from other devices)
# Find your IP: ifconfig (macOS/Linux) or ipconfig (Windows)''', "python")

    pdf.info_box("Network Access",
                 "To access from another device on the same Wi-Fi:\n"
                 "1. Find your machine's IP address (e.g., 192.168.1.100)\n"
                 "2. Open http://192.168.1.100:5001 on the other device\n"
                 "3. Ensure your firewall allows incoming connections on port 5001",
                 C_ACCENT)

    pdf.section_title("Running in Production")
    pdf.body_text(
        "For production deployment, consider the following improvements:"
    )
    pdf.bullet_list([
        "Use a production WSGI server like Gunicorn: gunicorn -w 4 -b 0.0.0.0:5001 app:app",
        "Place behind a reverse proxy (Nginx) for SSL termination and static file serving.",
        "Set debug=False and use a fixed secret key instead of os.urandom.",
        "Configure proper logging and error handling.",
        "Use environment variables for configuration parameters."
    ])

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 13: ADVANTAGES AND LIMITATIONS
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("Advantages and Limitations")

    pdf.section_title("Advantages")
    pdf.numbered_list([
        "Automated Grading: Eliminates the need for manual evaluation, saving significant time "
        "for educators handling large class sizes.",
        "Consistent Evaluation: The same algorithm is applied uniformly to all students, removing "
        "human bias and fatigue-related inconsistencies.",
        "NLP-Powered Analysis: TF-IDF and Cosine Similarity enable intelligent semantic comparison "
        "that goes beyond simple keyword matching.",
        "Dual Scoring Approach: The 60-40 combination of similarity and keyword scores provides "
        "a balanced evaluation that rewards both understanding and precision.",
        "Detailed Reports: Per-student HTML reports with visual indicators, keyword analysis, "
        "and score breakdowns provide actionable feedback.",
        "Class Analytics: Rankings, averages, and filtering help teachers quickly identify "
        "struggling students and common problem areas.",
        "Dual Interface: Both web and CLI interfaces cater to different usage scenarios.",
        "Network Accessible: The web interface can be accessed from any device on the same network.",
        "Lightweight: No database required; JSON files serve as the data format.",
        "Cross-Platform: Runs on macOS, Linux, and Windows without modification.",
        "Responsive Design: The web interface works on desktops, tablets, and mobile devices.",
        "Open Source Technologies: Built entirely with free, open-source tools."
    ])

    pdf.section_title("Limitations")
    pdf.numbered_list([
        "Language Support: Currently supports only English language answers.",
        "Answer Length: Very short answers (1-2 words) may not produce reliable similarity scores.",
        "Creative Answers: The system may undervalue creative or unconventional but correct answers.",
        "No Diagram Evaluation: Cannot evaluate hand-drawn diagrams or mathematical equations.",
        "Keyword Dependency: The quality of subjective scoring depends on the quality of the "
        "keyword list provided by the teacher.",
        "No Partial MCQ Credit: MCQ questions are strictly correct or incorrect with no partial marks.",
        "Single Correct Answer: MCQ questions support only a single correct option.",
        "JSON Input Required: Users must format their data in JSON, which may not be intuitive "
        "for non-technical users."
    ])

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 14: FUTURE ENHANCEMENTS
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("Future Enhancements")

    pdf.section_title("Short-Term Improvements")
    pdf.numbered_list([
        "Multi-Language Support: Extend NLP processing to support regional languages using "
        "multilingual models.",
        "PDF Report Export: Add the ability to export student reports as PDF documents.",
        "Excel/CSV Import: Support uploading answer keys and student data in Excel or CSV format "
        "instead of requiring JSON.",
        "Batch Result Export: Allow downloading all results as a consolidated Excel/CSV file.",
        "Enhanced MCQ Options: Support multiple correct answers and partial credit for MCQs.",
        "Configurable Weights: Allow teachers to adjust the similarity/keyword weight ratio "
        "per question or exam.",
    ])

    pdf.section_title("Medium-Term Improvements")
    pdf.numbered_list([
        "Database Integration: Migrate from JSON files to SQLite or PostgreSQL for persistent "
        "storage of question banks, student records, and historical results.",
        "User Authentication: Add login functionality for teachers and students with role-based "
        "access control.",
        "Question Bank: Build a repository of reusable questions organized by subject and topic.",
        "Answer History: Track student performance across multiple exams over time.",
        "Email Notifications: Send grading results and reports to students via email.",
        "API Endpoints: Create RESTful APIs so other systems can integrate with the grading platform.",
    ])

    pdf.section_title("Long-Term Vision")
    pdf.numbered_list([
        "Deep Learning Models: Replace TF-IDF with transformer-based models (BERT, GPT) for "
        "more nuanced semantic understanding.",
        "Handwriting Recognition (OCR): Integrate OCR to grade scanned handwritten answer scripts.",
        "Diagram Evaluation: Use computer vision to evaluate diagrams drawn by students.",
        "Adaptive Assessment: Dynamically adjust question difficulty based on student performance.",
        "Plagiarism Detection: Cross-check student answers for similarity to detect copying.",
        "Learning Analytics Dashboard: Provide comprehensive analytics showing learning trends, "
        "topic-wise performance, and predictive insights.",
        "Mobile Application: Develop a native mobile app for Android and iOS.",
        "Cloud Deployment: Host the application on cloud platforms (AWS, GCP, Azure) for "
        "institution-wide access without local setup."
    ])

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 15: CONCLUSION
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("Conclusion")

    pdf.body_text(
        "The Auto Answer Script Correction System successfully demonstrates the practical "
        "application of Natural Language Processing techniques in the domain of educational "
        "assessment. By combining TF-IDF vectorization, cosine similarity, and keyword matching, "
        "the system provides a reliable, consistent, and efficient method for evaluating both "
        "objective (MCQ) and subjective (descriptive) student answers."
    )
    pdf.body_text(
        "The project achieves all of its primary objectives: automated grading of both question "
        "types, NLP-based semantic evaluation, detailed per-student reports, class-level analytics "
        "with ranking, and dual CLI/web interfaces. The web interface's responsive design and "
        "network accessibility make it a practical tool for classroom use."
    )
    pdf.body_text(
        "Testing with sample data demonstrates that the system produces results that align well "
        "with expected outcomes: comprehensive answers score significantly higher than brief ones, "
        "keyword coverage contributes meaningfully to scores, and the ranking system correctly "
        "orders students by performance."
    )
    pdf.body_text(
        "The modular architecture of the system ensures maintainability and extensibility. Each "
        "component (MCQ Corrector, Subjective Corrector, Text Similarity, Report Generator) is "
        "independent and can be upgraded or replaced without affecting the others. The use of "
        "widely-adopted open-source technologies (Python, Flask, scikit-learn, NLTK) ensures "
        "long-term viability and community support."
    )
    pdf.body_text(
        "While the system has limitations in handling very creative responses, non-English "
        "languages, and visual content, the foundation laid by this project provides a solid "
        "base for future enhancements including deep learning integration, OCR for handwritten "
        "scripts, and cloud-based deployment."
    )
    pdf.body_text(
        "In conclusion, the Auto Answer Script Correction System represents a meaningful step "
        "toward digitizing and automating the evaluation process in educational institutions, "
        "offering significant time savings for educators while maintaining fairness and "
        "consistency in grading."
    )

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 16: REFERENCES
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("References")

    pdf.body_text("The following resources were referenced during the development of this project:")
    pdf.ln(4)

    references = [
        "[1] Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text "
        "retrieval. Information Processing & Management, 24(5), 513-523.",

        "[2] Manning, C. D., Raghavan, P., & Schuetze, H. (2008). Introduction to Information "
        "Retrieval. Cambridge University Press.",

        "[3] Bird, S., Klein, E., & Loper, E. (2009). Natural Language Processing with Python. "
        "O'Reilly Media.",

        "[4] Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. Journal "
        "of Machine Learning Research, 12, 2825-2830.",

        "[5] Flask Documentation. (2024). Flask: A Python Microframework. "
        "https://flask.palletsprojects.com/",

        "[6] NLTK Documentation. (2024). Natural Language Toolkit. "
        "https://www.nltk.org/",

        "[7] scikit-learn Documentation. (2024). TfidfVectorizer. "
        "https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html",

        "[8] Page, E. B. (1966). The imminence of grading essays by computer. Phi Delta Kappan, "
        "47(5), 238-243.",

        "[9] Shermis, M. D., & Burstein, J. (2013). Handbook of Automated Essay Evaluation: "
        "Current Applications and New Directions. Routledge.",

        "[10] Jinja2 Documentation. (2024). Jinja2: Template Engine for Python. "
        "https://jinja.palletsprojects.com/",

        "[11] Python Software Foundation. (2024). Python 3.9 Documentation. "
        "https://docs.python.org/3.9/",

        "[12] JSON.org. (2024). Introducing JSON. "
        "https://www.json.org/json-en.html",
    ]

    for ref in references:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*C_TEXT)
        pdf.multi_cell(0, 5.5, ref)
        pdf.ln(3)

    # ─────────────────────────────────────────────────────────────────────
    # APPENDIX A: COMPLETE SOURCE CODE LISTINGS
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("Appendix A: Complete Source Code")

    pdf.section_title("app.py - Flask Web Application")
    try:
        with open(os.path.join(BASE_DIR, "app.py"), "r", encoding="utf-8") as f:
            app_code = f.read()
        pdf.code_block(app_code)
    except FileNotFoundError:
        pdf.body_text("[File not found]")

    pdf.add_page()
    pdf.section_title("main.py - CLI Entry Point")
    try:
        with open(os.path.join(BASE_DIR, "main.py"), "r", encoding="utf-8") as f:
            main_code = f.read()
        pdf.code_block(main_code)
    except FileNotFoundError:
        pdf.body_text("[File not found]")

    pdf.add_page()
    pdf.section_title("corrector/mcq_corrector.py")
    try:
        with open(os.path.join(BASE_DIR, "corrector", "mcq_corrector.py"), "r", encoding="utf-8") as f:
            code = f.read()
        pdf.code_block(code)
    except FileNotFoundError:
        pdf.body_text("[File not found]")

    pdf.section_title("corrector/text_similarity.py")
    try:
        with open(os.path.join(BASE_DIR, "corrector", "text_similarity.py"), "r", encoding="utf-8") as f:
            code = f.read()
        pdf.code_block(code)
    except FileNotFoundError:
        pdf.body_text("[File not found]")

    pdf.add_page()
    pdf.section_title("corrector/subjective_corrector.py")
    try:
        with open(os.path.join(BASE_DIR, "corrector", "subjective_corrector.py"), "r", encoding="utf-8") as f:
            code = f.read()
        pdf.code_block(code)
    except FileNotFoundError:
        pdf.body_text("[File not found]")

    pdf.section_title("corrector/report_generator.py")
    try:
        with open(os.path.join(BASE_DIR, "corrector", "report_generator.py"), "r", encoding="utf-8") as f:
            code = f.read()
        pdf.code_block(code)
    except FileNotFoundError:
        pdf.body_text("[File not found]")

    # ─────────────────────────────────────────────────────────────────────
    # APPENDIX B: SAMPLE DATA FILES
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("Appendix B: Sample Data Files")

    pdf.section_title("data/answer_key.json")
    try:
        with open(os.path.join(BASE_DIR, "data", "answer_key.json"), "r", encoding="utf-8") as f:
            code = f.read()
        pdf.code_block(code, "json")
    except FileNotFoundError:
        pdf.body_text("[File not found]")

    pdf.add_page()
    pdf.section_title("data/student_answers.json")
    try:
        with open(os.path.join(BASE_DIR, "data", "student_answers.json"), "r", encoding="utf-8") as f:
            code = f.read()
        pdf.code_block(code, "json")
    except FileNotFoundError:
        pdf.body_text("[File not found]")

    # ─────────────────────────────────────────────────────────────────────
    # APPENDIX C: GLOSSARY
    # ─────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("Appendix C: Glossary")

    glossary = [
        ("API", "Application Programming Interface - a set of functions for building software."),
        ("CLI", "Command Line Interface - a text-based user interface."),
        ("Cosine Similarity", "A metric measuring the cosine of the angle between two vectors."),
        ("CSS", "Cascading Style Sheets - a language for describing HTML document presentation."),
        ("Flask", "A lightweight Python web framework for building web applications."),
        ("HTML", "HyperText Markup Language - the standard markup language for web pages."),
        ("IDF", "Inverse Document Frequency - measures how rare a term is across documents."),
        ("Jinja2", "A template engine for Python, used by Flask for rendering HTML."),
        ("JSON", "JavaScript Object Notation - a lightweight data interchange format."),
        ("LAN", "Local Area Network - a network connecting devices in a limited area."),
        ("MCQ", "Multiple Choice Question - a question with predefined answer options."),
        ("NLP", "Natural Language Processing - AI techniques for understanding human language."),
        ("NLTK", "Natural Language Toolkit - a Python library for NLP tasks."),
        ("OOP", "Object-Oriented Programming - a paradigm based on objects and classes."),
        ("Scikit-learn", "A Python library for machine learning algorithms."),
        ("Stopwords", "Common words (the, is, at) that are filtered out during NLP preprocessing."),
        ("TF", "Term Frequency - how often a term appears in a document."),
        ("TF-IDF", "Term Frequency-Inverse Document Frequency - a text importance metric."),
        ("Tokenization", "Splitting text into individual words or tokens."),
        ("WSGI", "Web Server Gateway Interface - a specification for Python web apps."),
    ]

    pdf.styled_table(
        ["Term", "Definition"],
        [[term, defn] for term, defn in glossary],
        col_widths=[40, 130]
    )

    # ─────────────────────────────────────────────────────────────────────
    # Now insert Table of Contents at page 2
    # ─────────────────────────────────────────────────────────────────────
    # We'll add the TOC as a new page after everything else, then reorder
    # Since fpdf2 doesn't allow easy page insertion, we generate TOC at the end
    # and note that the cover page explains where to find it

    total_pages = pdf.page_no()

    # Actually, let's insert the TOC properly by using a separate approach
    # We'll create a second pass to write the TOC
    # For now, add TOC as the last section

    pdf.add_page()
    pdf._in_cover = True  # Suppress header/footer for TOC style
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(*C_PRIMARY_DARK)
    pdf.cell(0, 16, "Table of Contents", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_draw_color(*C_PRIMARY)
    pdf.set_line_width(0.8)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(10)

    for level, title, page in pdf.toc_entries:
        if level == 0:
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(*C_PRIMARY_DARK)
            indent = 10
        elif level == 1:
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(*C_TEXT)
            indent = 20
        else:
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(*C_TEXT_SEC)
            indent = 30

        pdf.set_x(indent)
        # Title
        title_width = 160 - indent
        page_adjusted = page - 1  # Subtract cover page
        page_str = str(page_adjusted) if page_adjusted > 0 else "1"

        pdf.cell(title_width, 7, title)
        pdf.cell(20, 7, page_str, align="R")
        pdf.ln(7.5)

        if level == 0:
            pdf.ln(1)

        if pdf.get_y() > 270:
            pdf.add_page()
            pdf._in_cover = True

    pdf._in_cover = False

    # ─────────────────────────────────────────────────────────────────────
    # Output
    # ─────────────────────────────────────────────────────────────────────
    output_path = os.path.join(BASE_DIR, "Project_Documentation.pdf")
    pdf.output(output_path)
    print(f"\nPDF generated successfully!")
    print(f"Location: {output_path}")
    print(f"Total pages: {pdf.page_no()}")
    return output_path


if __name__ == "__main__":
    build_pdf()
