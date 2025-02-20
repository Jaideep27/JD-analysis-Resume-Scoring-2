# JD-analysis-Resume-Scoring-2🎯

An intelligent FastAPI application leveraging Google's Gemini AI models to automate resume evaluation and job description analysis. The system provides two main functionalities: job description criteria extraction and resume scoring.

## Project Structure 📁

```
JD insights & Resume Scoring/
├── models/
│   ├── __pycache__/
│   ├── config.py               # Configuration settings
│   ├── criteria_type.py        # Enum for criteria categories
│   ├── resume_scorer.py        # Resume evaluation logic
│   └── text_extractor.py       # PDF/DOCX text extraction
├── routes/
│   ├── __pycache__/
│   └── task_routes.py          # API route definitions
├── service/
│   ├── __pycache__/
│   ├── extract_criteria_service.py  # JD analysis implementation
│   └── score_resume_service.py      # Resume scoring implementation
├── Job_Descriptions/           # Storage for job description files
├── Resumes/                    # Storage for resume files
├── task_1 (Sample_Outputs)/    # Sample outputs from JD analysis
├── task_2 (Sample_Outputs)/    # Sample outputs from resume scoring
├── .gitignore                  # Git ignore rules
├── main.py                     # Application entry point
└── requirements                # Project dependencies
```

## Features ⚡

### 1. Job Description Analysis
Extracts key ranking criteria from job descriptions using the Gemini-2.0 Flash model.

**API Endpoint:**
```http
POST /extract_criteria
```

**Input:**
- File (PDF/DOCX)
- Criteria Type (skills, experience, certifications, qualifications, education, tools, languages, responsibilities, benefits, company culture, or overall)

**Gemini Prompt Template:**
```python
# For overall analysis
"""
Extract key ranking criteria (skills, experience, certifications, qualifications) 
from the following job description.:

{text}
"""

# For specific criteria type
"""
Extract key criteria related to {criteria_type}  
from the following job description. Return them as a list.
Only include the actual criteria without any explanatory text or headings:

{text}
"""
```

### 2. Resume Scoring System
Evaluates resumes against specified criteria using the Gemini-Pro model for scoring.

**API Endpoint:**
```http
POST /score_resume
```

**Input:**
- Multiple resume files (PDF/DOCX)
- Criteria list (comma-separated)

**Gemini Prompt Template:**
```python
"""
You are an expert HR professional with extensive experience in technical hiring. 
Evaluate this resume against each criterion on a scale of 0-5.

Scoring Guidelines:
5 - Exceptional match
4 - Strong match
3 - Good match
2 - Fair match
1 - Poor match
0 - No match

Criteria to evaluate:
{formatted_criteria}

Resume Text:
{text}

Please provide the scores for each criterion in this exact format (maintain exact criterion names):
{
    {', '.join(f'"{criterion}": <score>' for criterion in criteria_list)}
}
"""
```

## Installation 🚀

1. Clone the repository
```bash
git clone <repository-url>
cd JD insights & Resume Scoring
```

2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements
```

4. Set up environment variables
```bash
# Create .env file with your Gemini API key
GEMINI_API_KEY=your_api_key_here
```

## API Usage 💻

### Extract Criteria from Job Description
```python
import requests

url = "http://localhost:8000/extract_criteria"
files = {
    "file": ("job_description.pdf", open("job_description.pdf", "rb"))
}
params = {
    "criteria_type": "skills"  # Optional
}
response = requests.post(url, files=files, params=params)
print(response.json())
```

### Score Resumes Against Criteria
```python
import requests

url = "http://localhost:8000/score_resume"
files = [
    ("files", ("resume1.pdf", open("resume1.pdf", "rb"))),
    ("files", ("resume2.pdf", open("resume2.pdf", "rb")))
]
data = {
    "criteria": "Python,Machine Learning,Cloud Computing"
}
response = requests.post(url, files=files, data=data)
print(response.json())
```

### Download Results
```python
import requests

url = "http://localhost:8000/download/resume_scores_20250220_120145.csv"
response = requests.get(url)
with open("resume_scores.csv", "wb") as f:
    f.write(response.content)
```

## Sample Outputs 📊

### Job Description Analysis Output (JSON)
```json
{
  "criteria": [
    "LLM Expertise",
    "RAG & Vector Databases",
    "Azure AI Services",
    "MLOps & CI/CD",
    "Database Proficiency",
    "Libraries & Frameworks"
  ],
  "criteria_type": "skills"
}
```

### Resume Scoring Results (CSV)

| Candidate Name | BTech CSE Graduate | 6 months internship experience | Strong foundation in AI | Total Score |
|---------------|-------------------|------------------------------|----------------------|-------------|
| Charan        | 5                 | 4                           | 3                    | 12          |
| Ganesh        | 5                 | 0                           | 2                    | 7           |
| Ganga         | 5                 | 0                           | 2                    | 7           |
| Jaideep       | 5                 | 4                           | 4                    | 13          |
| Kowshik       | 5                 | 3                           | 4                    | 12          |
| Vivek         | 5                 | 1                           | 0                    | 6           |

## Running the Application 🚀

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

Access Swagger Documentation:
- http://localhost:8000/docs

## Technical Details

### Configuration
- Upload and output directories are managed in `config.py`
- Maximum score is set to 5
- Supported file formats: PDF and DOCX

### Text Extraction
The application supports extracting text from:
- PDF files using pdfplumber
- DOCX files using python-docx

### Scoring Algorithm
- Each criterion is scored on a scale of 0-5
- Scores are validated to ensure they're within the acceptable range
- Total score is calculated as the sum of individual criterion scores

### Error Handling 🛠️

The system handles various errors including:
- Invalid file formats
- File processing errors
- AI model response parsing
- Missing criteria or files
- Secure file system operations

## Security Features 🔒

- Temporary file cleanup after processing
- Input validation for all parameters
- Secure file handling with proper permissions
- Environment variable protection for API keys
- Error handling to prevent information leakage

## Dependencies

Main dependencies include:
- FastAPI for the API framework
- Google Generative AI Python SDK
- pdfplumber for PDF text extraction
- python-docx for DOCX handling
- pandas for data manipulation
- python-dotenv for environment management

## Support 💬

For questions and support, please open an issue in the repository.
