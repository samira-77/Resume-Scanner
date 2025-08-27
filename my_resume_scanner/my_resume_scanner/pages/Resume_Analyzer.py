
import streamlit as st
import pandas as pd
import os
import re
import nltk
import spacy
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader
from streamlit_extras.metric_cards import style_metric_cards

nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = ["python", "java", "sql", "machine learning", "excel", "communication", "project management", "power bi", "r", "data analysis", "cloud", "aws", "azure"]

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

def preprocess_text(text):
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

def extract_skills(text):
    return [skill for skill in SKILL_KEYWORDS if skill in text.lower()]

def extract_experience(text):
    text = text.lower()
    total_experience = 0
    years_set = set()
    exp_matches = re.findall(r'(\d+)\s*(?:\+)?\s*(?:years?|yrs?)', text)
    numeric_exp = [int(x) for x in exp_matches]
    if numeric_exp:
        total_experience = max(total_experience, max(numeric_exp))
    range_matches = re.findall(r'(\d+)\s*[\u2013\-to]+\s*(\d+)\s*(?:years?|yrs?)', text)
    for start, end in range_matches:
        try:
            total_experience = max(total_experience, int(end))
        except:
            continue
    date_matches = re.findall(r'(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]\s+)?(\d{4})\s[\u2013\-to]+\s*(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s+)?(\d{4}|present)', text)
    for start_year, end_year in date_matches:
        try:
            start_year = int(start_year)
            end_year = datetime.now().year if end_year == 'present' else int(end_year)
            if 1950 <= start_year <= end_year <= datetime.now().year + 1:
                for yr in range(start_year, end_year):
                    years_set.add(yr)
        except:
            continue
    total_experience = max(total_experience, len(years_set))
    return total_experience

def extract_experience_requirements(text):
    text = text.lower()
    range_match = re.search(r'(\d+)\s*(?:\+)?\s*(?:[\-\u2013to]{1,3})\s*(\d+)\s*(?:years?|yrs?)', text)
    if range_match:
        return int(range_match.group(1)), int(range_match.group(2))
    single_match = re.search(r'(\d+)\s*(?:\+)?\s*(?:years?|yrs?)', text)
    if single_match:
        return int(single_match.group(1)), int(single_match.group(1)) + 2
    return 0, 0

def check_ats_format(text):
    issues = []
    score = 100  # Start with perfect score
    
    # Check for tables/columns
    if re.search(r'\n\s*\|', text):
        issues.append("Avoid using tables or columns in the resume.")
        score -= 30
    
    # Check for required sections
    required_sections = ["experience", "education", "skills"]
    missing_sections = [section for section in required_sections if section not in text.lower()]
    if missing_sections:
        issues.append(f"Missing common resume headings: {', '.join(missing_sections)}")
        score -= 20 * len(missing_sections)
    
    # Check for contact information
    if not re.search(r'(phone|contact|email|e-mail|mobile)', text.lower()):
        issues.append("Missing contact information")
        score -= 15
    
    # Check for proper dates format
    if re.search(r'\d{1,2}/\d{1,2}/\d{2,4}', text):
        issues.append("Use full month names instead of numeric dates (e.g., 'January 2020' instead of '1/2020')")
        score -= 10
    
    return issues, max(0, score)  # Ensure score doesn't go below 0

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="AI Resume Screener", layout="wide")

# --- Robotic Illustration ---
st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=100)
st.title("🤖 AI-powered Resume Screening and Ranking System")

with st.sidebar:
    st.markdown("##  Navigation")
    menu = ["📝 Jobs", "👤 Candidates", "🔍 Matching"]
    choice = st.radio("Select View", menu, label_visibility="collapsed")

if choice.endswith("Jobs"):
    st.header("📝 Upload Job Descriptions")
    job_desc_files = st.file_uploader("Upload Job Descriptions (Text/PDF)", type=["txt", "pdf"], accept_multiple_files=True)

    if job_desc_files:
        job_descs = {}
        for job_file in job_desc_files:
            text = extract_text_from_pdf(job_file) if job_file.type == "application/pdf" else job_file.getvalue().decode("utf-8")
            job_descs[job_file.name] = preprocess_text(text)
        st.session_state["job_descriptions"] = job_descs
        st.success("✅ Job descriptions uploaded successfully!")

elif choice.endswith("Candidates"):
    st.header("👤 Upload Candidate Resumes")
    resume_files = st.file_uploader("Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True)

    if resume_files:
        resumes = {}
        for resume_file in resume_files:
            text = extract_text_from_pdf(resume_file)
            resumes[resume_file.name] = preprocess_text(text)
        st.session_state["resumes"] = resumes
        st.success("✅ Resumes uploaded successfully!")

elif choice.endswith("Matching"):
    st.header("🔍 Resume Matching and Feedback")

    if "job_descriptions" in st.session_state and "resumes" in st.session_state:
        job_names = list(st.session_state["job_descriptions"].keys())
        selected_job = st.selectbox("Select a Job Description", job_names)

        if selected_job:
            job_text = st.session_state["job_descriptions"][selected_job]
            resume_texts = st.session_state["resumes"]

            job_skills = extract_skills(job_text)
            job_exp_min, job_exp_max = extract_experience_requirements(job_text)

            vectorizer = TfidfVectorizer()
            job_vector = vectorizer.fit_transform([job_text])
            resume_vectors = vectorizer.transform(resume_texts.values())

            scores = cosine_similarity(job_vector, resume_vectors).flatten()
            ranked_resumes = sorted(zip(resume_texts.items(), scores), key=lambda x: x[1], reverse=True)

            st.subheader("📊 Resume Screening Results")

            for i, ((resume_name, resume_text), score) in enumerate(ranked_resumes[:10], start=1):
                resume_skills = extract_skills(resume_text)
                resume_exp = extract_experience(resume_text)
                ats_issues, ats_score = check_ats_format(resume_text)

                skill_match = len(set(job_skills).intersection(resume_skills)) / len(job_skills) if job_skills else 0

                # Improved experience matching calculation
                if job_exp_min == 0 and job_exp_max == 0:
                    experience_match = 0.7
                elif resume_exp >= job_exp_max:
                    experience_match = 1.0  # Full points for meeting or exceeding max
                elif resume_exp >= job_exp_min:
                    if job_exp_max>job_exp_min:
                        experience_match = 0.7 + 0.3 * ((resume_exp - job_exp_min) / (job_exp_max - job_exp_min))
                    else:
                        experience_match = 0.9
                elif resume_exp >0:
                    experience_match = 0.3 * (resume_exp  / job_exp_min)
                    
                        
                else:
                    # Below minimum - scale down more aggressively
                    experience_match = 0.0 

                overall_score = round((skill_match * 0.5 + experience_match * 0.3 + (ats_score/100) * 0.2) * 100, 2)

                st.markdown(f"""
                    <div class="resume-box">
                        <h4>{i}. {resume_name}</h4>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                col1.metric("Skill Match", f"{round(skill_match * 100)}%")
                col2.metric("Experience Match", f"{round(experience_match * 100)}%")
                col3.metric("ATS Score", f"{ats_score}%")
                style_metric_cards()

                st.markdown(f"""
                    <div class="overall-score-box">
                        Overall Score: {overall_score}%
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("🧠 Feedback & Suggestions:")
                if len(set(job_skills) - set(resume_skills)) > 0:
                    missing = ", ".join(set(job_skills) - set(resume_skills))
                    st.warning(f"🧩 Missing key skills: {missing}. Consider adding them.")

                if resume_exp < job_exp_min:
                    st.warning(f"🕒 This job prefers {job_exp_min}+ years. Your resume shows only {resume_exp} year(s).")
                elif job_exp_max > job_exp_min and resume_exp < job_exp_max:
                    st.info(f"ℹ Ideal experience range is {job_exp_min}-{job_exp_max} years. You have {resume_exp} years.")

                if ats_issues:
                    for issue in ats_issues:
                        st.error(f"⚠ {issue}")
                else:
                    st.success("✅ ATS formatting looks good!")

                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("⚠ Please upload job descriptions and resumes first.")

# ------------------- UI Styling -------------------
# Keep your full Python logic as it is (unchanged)
# -------------------- Streamlit App Code --------------------

# ------------------- UI Styling with Dark Blue Text -------------------
st.markdown("""
<style>
body, .stApp {
    background-color: #fefefe !important;
    color: #0f172a !important;  /* DARK BLUE TEXT */
    font-family: 'Segoe UI', sans-serif;
}

h1, h2, h3, h4 {
    background: linear-gradient(90deg, #0f172a, #1e3a8a);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
}

[data-testid="stSidebar"] {
   background: #f0f4f8 !important;
   border-right: 1px solid #e2e8f0;
}

[data-testid="stRadio"] label {
    color: #0f172a !important; /* Dark Blue for radio labels */
    background-color: #e2e8f0;
    padding: 10px 15px;
    border-radius: 8px;
    margin: 6px 0;
    transition: all 0.3s;
}
[data-testid="stRadio"] label:hover {
    background-color: #cbd5e1 !important;
}
[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
    background-color: #1e3a8a !important;
    color: white !important;
}

[data-testid="stFileUploader"] {
    border: 2px dashed #cbd5e1 !important;
    border-radius: 12px !important;
    padding: 20px !important;
    background-color: #ffffff !important;
    color: #0f172a !important;
}

[data-testid="metric-container"] {
    background: #ffffff !important;
    border-radius: 12px !important;
    padding: 15px !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    border: 1px solid #e2e8f0 !important;
}

[data-testid="stMetricValue"] {
    color: #1e3a8a !important; /* Dark Blue */
    font-size: 24px !important;
    font-weight: 700 !important;
}

[data-testid="stMetricLabel"] {
    color: #334155 !important; /* Muted Dark Blue */
    font-size: 14px !important;
    font-weight: 500 !important;
}

.overall-score-box {
    background: linear-gradient(135deg, #ffffff, #f1f5f9) !important;
    border: 1px solid #cbd5e1 !important;
    padding: 16px;
    margin: 10px 0 30px 0;
    border-radius: 12px;
    color: #1e3a8a !important;
    font-weight: bold;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    font-size: 20px;
}

.stButton>button {
    background: linear-gradient(90deg, #1e3a8a, #06b6d4) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    transition: all 0.3s;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(30, 58, 138, 0.3); /* darker blue glow */
}

.resume-box {
    background: #ffffff;
    padding: 24px;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    margin: 24px 0;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04);
}
.resume-box h4 {
    color: #0f172a !important;
    font-weight: 600;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)
