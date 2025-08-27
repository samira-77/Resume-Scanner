import streamlit as st
from PIL import Image

# Set up the page
st.set_page_config(page_title="AI Resume Scanner", layout="wide")

# Hide top navbar and padding
st.markdown("""
    <style>
    header {visibility: hidden;}
    .main {
        padding-top: 0rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Custom CSS styles
st.markdown("""
    <style>
    html, body, [data-testid="stApp"] {
        background: linear-gradient(to right, #141e30, #243b55);
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    .title-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .title {
        font-size: 4.5rem;
        font-weight: bold;
        color: #00eaff;
        text-shadow: 0 0 15px #00eaff;
        margin-bottom: 1rem;
        margin-top: 0rem;
    }

    .description {
        font-size: 1.9rem;
        font-weight: bold;
        background-color: rgba(0, 0, 0, 0.6);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0, 234, 255, 0.5);
        text-align: center;
        width:600px;
        height:300px;
    }

    .stButton > button {
        background: #00eaff;
        color: black;
        font-weight: bold;
        padding: 1.0rem 2rem;
        border: none;
        border-radius: 10px;
        transition: all 0.3s ease;
        font-size: 1rem;
        margin-top: 2rem;
    }

    .stButton > button:hover {
        background: #0288d1;
        color: white;
        box-shadow: 0 0 15px #00eaff;
    }

    .robot-container {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 0 40px rgba(0,234,255,0.2);
        margin-top:10px;
    }

    .robot-container::before {
        content: "";
        position: absolute;
        width: 300px;
        height: 300px;
        border: 2px solid #00eaff;
        border-radius: 50%;
        animation: pulseRing 2.5s infinite ease-in-out;
        z-index: 0;
    }

    .floating-icon {
        position: absolute;
        width: 32px;
        height: 32px;
        animation: float 4s ease-in-out infinite;
        opacity: 0.8;
    }

    .icon1 { top: 10%; left: 10%; animation-delay: 0s; }
    .icon2 { top: 20%; right: 15%; animation-delay: 1s; }
    .icon3 { bottom: 15%; left: 20%; animation-delay: 2s; }

    @keyframes pulseRing {
        0% { transform: scale(0.95); opacity: 0.7; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(0.95); opacity: 0.7; }
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }
    </style>
""", unsafe_allow_html=True)

# Load robot image
image_path = "image.png"
try:
    robot_img = Image.open(image_path)
except Exception:
    robot_img = None

# Page session state
if 'page' not in st.session_state:
    st.session_state.page = "home"

# --- Home Page ---
if st.session_state.page == "home":
    col1, col2 = st.columns([2, 1.3])

    with col1:
        st.markdown('<div class="title-row">', unsafe_allow_html=True)
        st.markdown('<div class="title">AI Resume Scanner</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
            <div class="description">
                Our AI-powered resume scanner evaluates your resume in real-time, 
                analyzing formatting, keyword match, and readability to ensure it meets 
                industry standards.
            </div>
        """, unsafe_allow_html=True)

        btn1, btn2, btn3 = st.columns([1, 1, 1])
        with btn1:
            if st.button("Analyze My Resume"):
                st.switch_page("pages/Resume_Analyzer.py")  # <--- This is the integration part
        with btn2:
            if st.button("Resources"):
                st.session_state.page = "resources"
        with btn3:
            if st.button("Create Resume"):
                st.switch_page("pages/Create_Resume.py")

    with col2:
        st.markdown('<div class="robot-container">', unsafe_allow_html=True)
        st.markdown("""
            <img class="floating-icon icon1" src="https://img.icons8.com/fluency/48/resume.png"/>
            <img class="floating-icon icon2" src="https://img.icons8.com/fluency/48/artificial-intelligence.png"/>
            <img class="floating-icon icon3" src="https://img.icons8.com/fluency/48/cloud.png"/>
        """, unsafe_allow_html=True)
        if robot_img:
            st.image(robot_img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- Resources Page ---
# --- Resources Page ---
elif st.session_state.page == "resources":
    st.markdown('<h1 style="color:#00eaff;">📄 How to Write a Resume</h1>', unsafe_allow_html=True)

    st.markdown("""
    - *Keep it concise* (1–2 pages max).  
    - *Use a clean format* with consistent fonts and bullet points.  
    - *Highlight relevant experience* for the job you're applying for.  
    - *Use keywords* from the job description to pass ATS filters.  
    - *Proofread* to avoid grammatical mistakes.

    # 📄 How to Write a Resume

    ## ✨ Why Your Resume Matters
    Your resume is more than just a document—it's your personal marketing tool. It should tell a compelling story about your skills, achievements, and career journey in just a few seconds.

    > Recruiters spend an average of 6 seconds scanning a resume before deciding whether to proceed with a candidate. That’s why clarity, conciseness, and impact are key.

    This guide will help you craft a resume that stands out, impresses hiring managers, and lands you interviews.

    ---

    ## 👉 Choose the Right Resume Format
    There are three main resume formats. Choose one based on your experience level:

    ### ✅ 1. Chronological Resume (Most Common)
    - *Best for:* Professionals with consistent work experience
    - Lists jobs in reverse order (most recent first)
    - Ideal for showcasing career growth

    ### ✅ 2. Functional Resume (Skill-Based)
    - *Best for:* Freshers, career changers, or those with gaps
    - Focuses on skills rather than work experience
    - Ideal if you lack extensive work history

    ### ✅ 3. Combination Resume (Hybrid)
    - *Best for:* Experienced professionals & specialized roles
    - Highlights both skills and experience
    - Perfect if you have strong skills + diverse experience

    > 💡 *PRO TIP:* Most applicants should stick to the Chronological format since it's ATS (Applicant Tracking System) friendly.

    ---

    ## 👉 Resume Structure: What to Include?

    ### ✅ 1. Header
    - Full Name
    - Professional Email (Avoid fancy emails like "coolguy123@gmail.com")
    - Phone Number
    - LinkedIn Profile & Portfolio (if applicable)

    *Example:*

    Jane Doe  
    jane.doe@email.com | +91 9876543210  
    linkedin.com/in/janedoe | 🌐 janedoe.dev

    ### ✅ 2. Professional Summary / Objective
    *For experienced candidates:* Write a 2-3 line summary highlighting your expertise, key skills, and achievements.  
    *For freshers:* Mention your skills, educational background, and career aspirations.

    *Example (Experienced):*  
    👉 Results-driven Software Engineer with 5+ years of experience in Python, AI, and cloud computing. Developed scalable applications, reducing downtime by 30% and increasing efficiency.

    *Example (Fresher):*  
    💡 Passionate Computer Science graduate with strong Python and Web Development skills. Eager to apply my knowledge in a dynamic environment to build innovative solutions.

    > 💡 *PRO TIP:* Avoid generic statements like "Hardworking and motivated individual..." Be specific!

    ### ✅ 3. Key Skills (Technical & Soft Skills)
    List 6–10 skills relevant to the job you’re applying for.

    *Example (Software Engineer):*

    🖥 **Technical Skills:**
    - Python, Java, C++
    - Web Development (React, Node.js)
    - Machine Learning & AI (TensorFlow, Scikit-Learn)
    - Database Management (SQL, MongoDB)
    - Cloud Platforms (AWS, Azure, GCP)

    🤝 **Soft Skills:**
    - Problem-solving
    - Team Collaboration
    - Communication
    - Leadership

    > 💡 *PRO TIP:* Use keywords from the job description to pass ATS screening!

    ### ✅ 4. Work Experience (STAR Method)
    *Structure:*
    - Job Title – Company Name | Dates (Month, Year – Present)
    - Location (Optional)
    - Key Responsibilities & Achievements (Use Bullet Points & Action Words)

    > 💡 Use the STAR method:  
    *S* – Situation (What was the challenge?)  
    *T* – Task (What needed to be done?)  
    *A* – Action (What did you do?)  
    *R* – Result (What was the impact?)

    *Example:*

    📍 **Software Engineer – ABC Tech | Jan 2021 – Present**
    - Developed a cloud-based API that improved system efficiency by 40%.
    - Led a team of 5 developers to launch an AI-driven chatbot for customer support.
    - Optimized SQL queries, reducing database load time by 30%.

    🛠 **Bad Example:**
    - Worked on a web app.
    - Helped with bug fixing.
    - Used Python for coding.

    > 💡 *PRO TIP:* Quantify achievements with numbers & percentages!

    ### ✅ 5. Education
    *Example:*  
    - B.Tech in Computer Science – Basaveshwar Engineering College | 2025  
      Karnataka, India

    ### ✅ 6. Certifications & Achievements
    List relevant certifications that enhance your profile.

    *Example:*
    - AWS Certified Solutions Architect – 2024
    - Data Science with Python – Coursera

    > 💡 *PRO TIP:* If you’re a fresher, include hackathons, coding competitions, or open-source contributions!

    ### ✅ 7. Projects (For Freshers & Tech Roles)
    If you lack work experience, highlight projects that showcase your skills.

    *Example:*
    - 👉 AI Resume Screener – Developed an AI-powered resume ranking system using NLP & Machine Learning.
    - 👉 E-Commerce Website – Built a full-stack React & Node.js shopping website with Stripe payment integration.

    > 💡 *PRO TIP:* Link your GitHub or portfolio for recruiters to explore your work!

    ---

    ## 👉 Resume Formatting Tips (Make It Look Professional!)
    - Keep It 1–2 Pages Max 🗜
    - Use Professional Fonts (Arial, Calibri, Times New Roman)
    - ✍ Font Size: 11–12pt for text, 14–16pt for headings
    - Margins: 1-inch on all sides
    - Use Bullet Points Instead of Large Paragraphs
    - 🛠 Save as PDF (Unless Stated Otherwise)

    ### ❌ Avoid These Mistakes:
    - Spelling & grammar errors (Use Grammarly!)
    - Using an outdated template
    - Lying about skills or experience

    ---

    ## 📉 Free Resume Templates & Tools
    💻 **Resume Builders:**
    - Canva (Modern templates)
    - Zety (AI-based suggestions)
    - Novoresume (Clean professional designs)

    ---

    ## 🚀 Craft a Resume That Gets You Hired!
    Follow these steps, customize your resume for each job, and highlight your best achievements to make a lasting impression.

    > 💡 Now go land that dream job!

    👉 [Read more: Indeed Resume Guide](https://in.indeed.com/career-advice/resumes-cover-letters/how-to-make-a-resume-with-examples)
    """)

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
