# Job Agent

ATS-optimized resume and cover letter generator powered by a multi-agent LLM pipeline.

## What It Does

- Parses a job description into structured hiring signals
- Scores resume-job fit with strengths, gaps, and positioning angles
- Rewrites resume content to align with the target role
- Generates a tailored cover letter
- Runs ATS-focused quality checks
- Exports resume and cover letter in PDF and Word (`.docx`)

## Tech Stack

- Backend: Python + Flask
- LLM routing: OpenRouter API
- Parsing: `PyPDF2`
- Document export: `reportlab` (PDF), `python-docx` (Word)
- Frontend: HTML/CSS/JS dashboard

## Project Structure

```text
job-agent/
├── agents/
│   ├── jd_parser.py
│   ├── match_scorer.py
│   ├── resume_rewriter.py
│   ├── cover_letter.py
│   └── quality_checker.py
├── utils/
│   ├── openrouter.py
│   └── pdf_parser.py
├── frontend/
│   └── index.html
├── orchestrator.py
├── app.py
├── requirements.txt
└── .env.example
```

## Architecture (Pipeline)

1. `jd_parser` -> extracts role title, keywords, skills, tone, and responsibilities
2. `match_scorer` -> evaluates fit and identifies gaps
3. `resume_rewriter` -> rewrites resume in ATS-friendly structure
4. `cover_letter` -> writes role/company-specific cover letter
5. `quality_checker` -> returns ATS score and improvement suggestions

The orchestrator (`orchestrator.py`) runs these steps sequentially and returns a unified JSON response.

## Setup

### 1) Clone

```bash
git clone https://github.com/gayu56/job-agent.git
cd job-agent
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure environment

Create a `.env` file in `job-agent/` using `.env.example`:

```bash
OPENROUTER_API_KEY=your-openrouter-key
OPENROUTER_MODEL_FAST=anthropic/claude-3.5-haiku
OPENROUTER_MODEL_STRONG=anthropic/claude-3.5-sonnet
```

## Run Locally

```bash
python app.py
```

Open:

- `http://127.0.0.1:5000/`

## API Endpoints

### `POST /analyze`

Analyzes resume + JD and returns:

- `jd_analysis`
- `match_score`
- `resume`
- `cover_letter`
- `quality_report`

Input (form-data):

- `company` (required)
- `jd_text` (required)
- `resume_text` (optional if `resume_pdf` provided)
- `resume_pdf` (optional if `resume_text` provided)

### `POST /export`

Exports generated content as PDF or Word.

Input (form-data):

- `type`: `resume` or `cover_letter`
- `format`: `pdf` or `docx`
- `company`
- `content`

## UI Highlights

- Left input panel for company, JD, and resume upload
- Right-side analytics dashboard:
  - Fit score
  - Keyword coverage
  - ATS score
  - Gaps and suggestions
- Download buttons for:
  - Resume -> PDF / Word
  - Cover letter -> PDF / Word

## Notes

- `.env` is git-ignored by default.
- If a model returns 404 from OpenRouter, switch model IDs in `.env`.
- For best outputs, use detailed job descriptions and resume text with metrics.
