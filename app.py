import os
import streamlit as st
from openai import OpenAI

from rag_resume import (
    extract_text_from_file,
    rewrite_resume_duties,
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="RAG-as-a-Service: Resume Duty Adjuster",
    page_icon="🧠",
    layout="centered",
)

st.title("🧠 RAG-as-a-Service: Resume Duty Adjuster (Interactive Edition)")

st.markdown(
    """
Upload your resume and paste the job qualifications.  

This tool will:

1. Rewrite **only** your job duties  
2. Clean the messy PDF formatting  
3. Output a clean resume  
4. Let you give **feedback**, then revise the resume again based on your comments  
"""
)

# --- Session state setup ---
if "updated_resume_text" not in st.session_state:
    st.session_state.updated_resume_text = ""
if "original_resume_text" not in st.session_state:
    st.session_state.original_resume_text = ""
if "job_description" not in st.session_state:
    st.session_state.job_description = ""

# -------- Upload + JD input --------
uploaded_file = st.file_uploader(
    "Upload your resume (PDF or DOCX)",
    type=["pdf", "docx"],
)

job_description = st.text_area(
    "Paste the job qualifications or job description",
    placeholder="Paste the job posting or bullet-point qualifications here...",
    height=200,
)

run_button = st.button("⚙️ Adjust Job Duties")

# ---------------------------
# STEP 1: INITIAL REWRITE
# ---------------------------
if run_button:
    if not uploaded_file:
        st.error("Please upload a resume file first.")
    elif not job_description.strip():
        st.error("Please paste the job qualifications or job description.")
    else:
        with st.spinner("Analyzing and adjusting your job duties..."):
            try:
                original_text = extract_text_from_file(uploaded_file)
                updated_text = rewrite_resume_duties(original_text, job_description)

                # Save for feedback loop
                st.session_state.original_resume_text = original_text
                st.session_state.job_description = job_description
                st.session_state.updated_resume_text = updated_text

                st.success("Done! Copy the revised content below OR give feedback to improve it. ✅")

            except Exception as e:
                st.error(f"Something went wrong: {e}")

# ---------------------------
# STEP 2: FEEDBACK + REVISION
# ---------------------------
if st.session_state.updated_resume_text:
    st.markdown("## ✏️ Give Feedback to Improve the Resume")

    feedback = st.text_area(
        "What would you like improved?",
        placeholder=(
            "Examples:\n"
            "- Make the bullets more concise\n"
            "- Add more leadership tone\n"
            "- Emphasize AI / ML ownership and thought leadership at Ad.net\n"
            "- Add stronger metrics\n"
            "- Make it sound more senior"
        ),
        height=150,
        key="feedback_input",
    )

    revise_button = st.button("🔄 Apply Feedback and Revise Again")

    # If you click revise, we update session_state.updated_resume_text
    if revise_button:
        if not feedback.strip():
            st.error("Please write some feedback before revising.")
        else:
            with st.spinner("Applying your feedback and revising the resume..."):
                try:
                    revision_prompt = f"""
You are an expert resume editor.

Here is the ORIGINAL resume:
\"\"\"
{st.session_state.original_resume_text}
\"\"\"

Here is the TARGET JOB DESCRIPTION:
\"\"\"
{st.session_state.job_description}
\"\"\"

Here is the AI's current revised resume:
\"\"\"
{st.session_state.updated_resume_text}
\"\"\"

Here is the USER FEEDBACK on how to improve it:
\"\"\"
{feedback}
\"\"\"

TASK:
Revise the resume AGAIN using the feedback, keeping:
- The cleaned formatting
- Titles, companies, and dates unchanged
- Only rewriting job duties and polishing phrasing
- Explicitly leaning into AI / ML ownership and thought leadership at Ad.net when requested.

OUTPUT:
Return the improved resume as clean plain text. No explanations.
"""
                    response = client.responses.create(
                        model="gpt-5-mini",
                        input=revision_prompt,
                    )
                    new_text = response.output_text

                    # Update state BEFORE we render the text area below
                    st.session_state.updated_resume_text = new_text
                    st.success("Updated! Scroll down to see the new revised resume. 🎉")

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

    # Show whatever is currently in session_state.updated_resume_text
    st.markdown("## 🔁 Revised Resume (AI Output)")
    st.text_area(
        "Updated Resume Text",
        value=st.session_state.updated_resume_text,
        height=400,
    )
