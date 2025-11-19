# 🧠 RAG-as-a-Service: Resume Duty Adjuster

A local interactive tool that:

- Accepts your resume (PDF or DOCX)
- Accepts a job description
- Uses OpenAI to **rewrite only your job duty bullets**
- Cleans messy extracted formatting
- Supports an **iterative feedback loop** so you can refine results
- Produces a clean text resume to paste into Word/Docs

Built with **Python, Streamlit, and OpenAI**.

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/rag-resume-duty-adjuster.git
cd rag-resume-duty-adjuster
```
### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows PowerShell
```
### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Setup your environment variables
```bash

cp .env.example .env
Edit .env:
OPENAI_API_KEY=sk-your-key-here
```

🧩 How It Works

- Upload Resume
  - PDF or DOCX → text extracted automatically.

- Paste Job Description
  - The target role’s requirements.

### AI Rewrite
The tool:
- Normalizes formatting
- Keeps titles, dates, companies the same
- Rewrites job duty bullets only
- Interactive Feedback Loop
  - You tell the AI what to adjust, and it regenerates the resume using:

### Original resume

- Job description
- Previous output
- Your feedback
- Copy Final Text
- Paste into your preferred resume editor.

### 🛠️ Technologies
- Python 3.x
- Streamlit
- OpenAI Responses API
- python-docx
- PyPDF2
