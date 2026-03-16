# Auto Answer Script Correction System

A Python-based automated answer script evaluation system that grades both **MCQ (Multiple Choice)** and **Subjective (Descriptive)** answers using Natural Language Processing (NLP) techniques.

## Features

- **MCQ Auto-Correction**: Exact match comparison with answer key
- **Subjective Answer Grading**: Uses TF-IDF + Cosine Similarity and keyword matching
- **Keyword-Based Scoring**: Checks for important terms in student answers
- **Detailed Reports**: Generates per-student HTML reports with question-wise scores
- **Web Interface**: Flask-based UI for uploading answer keys and student answers
- **CLI Mode**: Command-line interface for batch grading

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.9+ |
| NLP | scikit-learn (TF-IDF), NLTK |
| Web Framework | Flask |
| Templating | Jinja2 |
| Data Format | JSON |

## Project Structure

```
AutoAnswerCorrection/
├── main.py                  # CLI entry point
├── app.py                   # Flask web application
├── requirements.txt         # Python dependencies
├── corrector/
│   ├── __init__.py
│   ├── mcq_corrector.py     # MCQ grading logic
│   ├── subjective_corrector.py  # Subjective answer grading (NLP)
│   ├── text_similarity.py   # TF-IDF & cosine similarity utilities
│   └── report_generator.py  # HTML report generation
├── data/
│   ├── answer_key.json      # Model answers (MCQ + Subjective)
│   └── student_answers.json # Sample student responses
├── templates/
│   ├── index.html           # Web interface home page
│   ├── results.html         # Results display page
│   └── report.html          # Detailed report template
├── static/
│   └── style.css            # Stylesheet
└── reports/                 # Generated reports (auto-created)
```

## Installation

```bash
# 1. Navigate to project directory
cd AutoAnswerCorrection

# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLTK data (one-time)
python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"
```

## Usage

### Option 1: Command Line Interface

```bash
python3 main.py
```

This reads `data/answer_key.json` and `data/student_answers.json`, grades all students, and generates reports in the `reports/` folder.

### Option 2: Web Interface

```bash
python3 app.py
```

Open your browser and go to `http://127.0.0.1:5000`. You can:
1. Upload an answer key JSON file
2. Upload student answers JSON file
3. View results and download reports

## Data Format

### Answer Key (`answer_key.json`)

```json
{
  "subject": "Computer Science",
  "total_marks": 50,
  "questions": [
    {
      "id": 1,
      "type": "mcq",
      "question": "What does CPU stand for?",
      "correct_answer": "B",
      "marks": 2
    },
    {
      "id": 2,
      "type": "subjective",
      "question": "Explain what an operating system is.",
      "model_answer": "An operating system is system software...",
      "keywords": ["system software", "hardware", "resources", "user interface"],
      "marks": 10
    }
  ]
}
```

### Student Answers (`student_answers.json`)

```json
{
  "students": [
    {
      "roll_number": "CS001",
      "name": "Student Name",
      "answers": [
        { "question_id": 1, "answer": "B" },
        { "question_id": 2, "answer": "An operating system is a software..." }
      ]
    }
  ]
}
```

## How It Works

### MCQ Correction
- Direct string comparison (case-insensitive) between student answer and correct answer
- Full marks for correct, zero for incorrect

### Subjective Answer Correction
The system uses a hybrid scoring approach:

1. **TF-IDF Cosine Similarity (60% weight)**: Converts both model and student answers into TF-IDF vectors, then measures cosine similarity
2. **Keyword Matching (40% weight)**: Checks how many important keywords from the model answer appear in the student's response

### Grading Scale
| Score Range | Grade |
|-------------|-------|
| 90-100% | A+ |
| 80-89% | A |
| 70-79% | B+ |
| 60-69% | B |
| 50-59% | C |
| Below 50% | F |

## License

This project is created for academic/educational purposes.
