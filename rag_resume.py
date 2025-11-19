import os
from docx import Document
from PyPDF2 import PdfReader
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_text_from_file(uploaded_file) -> str:
    """
    Extract plain text from an uploaded PDF or DOCX.
    Streamlit gives us an UploadedFile object with a name and file-like buffer.
    """
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        pages_text = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages_text)

    elif file_name.endswith(".docx"):
        doc = Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")


def build_rewrite_prompt(resume_text: str, job_description: str) -> str:
    """
    Instructions for the model:
    - Fix formatting into a clean resume
    - Only change job duties content-wise
    """
    return f"""
You are a specialized resume rewriting engine and formatter.

GOALS:
1) Adjust ONLY the job duty bullet points so they better align with the target job qualifications.
2) Clean up and normalize the resume formatting into a tidy, modern, ATS-friendly layout.

FORMATTING RULES:
- Fix broken line breaks and spacing from the PDF (no one-word-per-line text).
- Use normal spacing between words (e.g., "Product Leader", not "P R O D U C T  L E A D E R").
- Use clear section headings like:
  - SUMMARY or TITLE (optional)
  - WORK EXPERIENCE
  - EDUCATION
  - SKILLS
- For each role, put the header on ONE line, for example:
  Job Title | Company | Location | Dates
- Under each role, use concise bullet points starting with "-" or "•".
- Do NOT output random single letters on their own lines.
- Keep everything in plain text (no markdown formatting needed beyond bullets).

CONTENT RULES:
- DO NOT change:
  - Job titles
  - Company names
  - Locations
  - Dates of employment
- DO NOT invent fake experience or obviously untrue skills.
- You MAY:
  - Rephrase existing bullets
  - Emphasize skills and responsibilities that match the target job
  - Add realistic, non-fabricated detail that could reasonably be inferred from the role
- Maintain a professional, confident tone.

INPUT RESUME (may be messy due to PDF extraction):
\"\"\" 
{resume_text}
\"\"\"

TARGET JOB QUALIFICATIONS:
\"\"\" 
{job_description}
\"\"\" 

OUTPUT:
Return the FULL UPDATED RESUME as clean, well-formatted plain text with:
- Normal spacing
- Logical sections
- Clean bullet lists for job duties

Do NOT include any explanation or commentary; output ONLY the resume.
"""


def rewrite_resume_duties(resume_text: str, job_description: str) -> str:
    """
    Call OpenAI to semantically adjust job duties and reformat the resume.
    """
    prompt = build_rewrite_prompt(resume_text, job_description)

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    updated_resume = response.output_text
    return updated_resume
