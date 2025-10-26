"""
PortfolioAI - Main Streamlit Application
CORE MVP: Upload resume -> Parse -> Generate portfolio + CV -> Download
"""

import os
import time
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import utilities
from utils.supabase_client import get_supabase_client
from utils.resume_parser import get_resume_parser
from utils.linkedin_scraper import get_linkedin_scraper
from utils.portfolio_generator import get_portfolio_generator
from utils.resume_generator import get_resume_generator
from utils.validators import FileUploadValidator
from utils.groq_client import get_groq_client

# Page config
st.set_page_config(
    page_title="PortfolioAI - Instant Personal Brand",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
def load_css():
    css_file = "assets/style.css"
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Initialize clients
try:
    supabase = get_supabase_client()
    resume_parser = get_resume_parser()
    linkedin_scraper = get_linkedin_scraper()
    portfolio_gen = get_portfolio_generator()
    resume_gen = get_resume_generator()
    groq_client = get_groq_client()
except Exception as e:
    st.error(f"⚠️ Failed to initialize services: {e}")
    st.info("💡 **For Local Development:** Make sure you have set up .env file with Supabase and Groq credentials")
    st.info("💡 **For Hugging Face Spaces:** Add secrets in Settings → Repository secrets:")
    st.code("""
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
    """)
    st.stop()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = None
if 'portfolio_html' not in st.session_state:
    st.session_state.portfolio_html = None
if 'resume_pdf' not in st.session_state:
    st.session_state.resume_pdf = None
if 'resume_docx' not in st.session_state:
    st.session_state.resume_docx = None
if 'subdomain' not in st.session_state:
    st.session_state.subdomain = None
# Authentication state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = False
if 'saved_portfolios' not in st.session_state:
    st.session_state.saved_portfolios = []
# Interview prep state
if 'show_mock_interview' not in st.session_state:
    st.session_state.show_mock_interview = False
if 'mock_interview_questions' not in st.session_state:
    st.session_state.mock_interview_questions = []
if 'show_career_coach' not in st.session_state:
    st.session_state.show_career_coach = False
# Career coach chat state
if 'career_coach_chat_history' not in st.session_state:
    st.session_state.career_coach_chat_history = []
if 'career_coach_mode' not in st.session_state:
    st.session_state.career_coach_mode = 'chat'  # 'chat' or 'topics'
# Q&A flow state
if 'qa_data' not in st.session_state:
    st.session_state.qa_data = {}
# LLM model selection
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = '70b'  # Default to best model


# ==================== LANDING PAGE ====================

def landing_page():
    """Landing page with 3 input options"""

    # Hero section
    st.markdown("""
    <div class="hero">
        <div style="font-size: 56px; font-weight: 700; margin-bottom: 20px; letter-spacing: -1px; background: linear-gradient(135deg, #FF0080, #7928CA, #0070F3); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            PortfolioAI
        </div>
        <h1 class="gradient-text">Your AI-Powered Career Companion</h1>
        <p style="font-size: 18px; margin-bottom: 10px;">Portfolio • Resume • Interview Prep • Career Coaching</p>
        <p style="color: #888; font-size: 14px;">From first draft to final offer—powered by advanced AI that understands your journey</p>
    </div>
    """, unsafe_allow_html=True)

    # Auth buttons or user info
    st.markdown("<br>", unsafe_allow_html=True)

    # Check if user is logged in
    if st.session_state.user_id and not st.session_state.demo_mode:
        # User is logged in - show user info and logout
        user_col1, user_col2, user_col3 = st.columns([2, 1, 1])

        with user_col1:
            # Welcome message with gradient styling
            user_email = st.session_state.user_email or "User"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(255,0,128,0.1), rgba(121,40,202,0.1));
                        border-radius: 12px; padding: 15px; border: 1px solid rgba(255,0,128,0.3);">
                <p style="margin: 0; font-size: 16px; color: #FF0080;">
                    👋 Welcome back, <strong>{user_email}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)

        with user_col2:
            if st.button("📁 My Portfolios", use_container_width=True, type="primary"):
                st.session_state.page = 'my_portfolios'
                st.rerun()

        with user_col3:
            if st.button("🚪 Logout", use_container_width=True):
                # Clear session state
                st.session_state.user_id = None
                st.session_state.user_email = None
                st.session_state.demo_mode = False
                st.session_state.saved_portfolios = []
                st.success("✅ Logged out successfully!")
                time.sleep(1)
                st.rerun()

    else:
        # User is NOT logged in - show auth options
        auth_col1, auth_col2, auth_col3 = st.columns([1, 1, 1])

        with auth_col1:
            if st.button("🎮 Try Demo Mode", use_container_width=True, type="primary"):
                st.session_state.demo_mode = True
                st.session_state.user_id = None
                st.info("✅ Demo mode activated! Your work won't be saved.")

        with auth_col2:
            if st.button("🔐 Sign In", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()

        with auth_col3:
            if st.button("✨ Sign Up Free", use_container_width=True):
                st.session_state.page = 'signup'
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🚀 Get Started - Choose Your Input Method")

    # Three columns for input options
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">📄</div>
            <h3>Upload Resume</h3>
            <p>PDF or Word document</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Choose file",
            type=['pdf', 'docx', 'doc'],
            key='resume_upload',
            label_visibility="collapsed"
        )

        if uploaded_file:
            is_valid, error = FileUploadValidator.validate_file(uploaded_file, uploaded_file.name)
            if not is_valid:
                st.error(f"❌ {error}")
            else:
                if st.button("🎨 Generate Portfolio", key='btn_upload', use_container_width=True):
                    process_resume_upload(uploaded_file)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🔗</div>
            <h3>LinkedIn Profile</h3>
            <p>Paste your profile link or text</p>
        </div>
        """, unsafe_allow_html=True)

        profile_text = st.text_area(
            "LinkedIn profile text",
            placeholder="Paste your LinkedIn profile:\n\n• LinkedIn URL (linkedin.com/in/yourname)\n• OR your full profile text\n• Professional summary\n• Work experience\n• Skills & Education\n\nCopy-paste anything from your LinkedIn!",
            height=180,
            key='linkedin_text',
            label_visibility="collapsed"
        )

        if profile_text:
            if st.button("🎨 Generate Portfolio", key='btn_linkedin', use_container_width=True):
                process_linkedin_input(profile_text)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">✨</div>
            <h3>Start from Scratch</h3>
            <p>5-minute Q&A</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Start Q&A", key='btn_qa', use_container_width=True):
            st.session_state.page = 'qa_flow'
            st.rerun()

    # How it works section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## 🚀 How It Works")
    st.markdown("<br>", unsafe_allow_html=True)

    how_col1, how_col2, how_col3 = st.columns(3)

    with how_col1:
        st.markdown("""
        <div style="text-align: center; padding: 30px 20px;">
            <div style="font-size: 48px; margin-bottom: 15px;">📤</div>
            <h3 style="color: #FF0080; margin-bottom: 10px;">1. Upload Your Info</h3>
            <p style="color: #A0A0A0; line-height: 1.6;">
                Upload your resume or paste your LinkedIn profile.
                Our AI parses it in seconds with 100% accuracy.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with how_col2:
        st.markdown("""
        <div style="text-align: center; padding: 30px 20px;">
            <div style="font-size: 48px; margin-bottom: 15px;">✨</div>
            <h3 style="color: #7928CA; margin-bottom: 10px;">2. AI Generates Assets</h3>
            <p style="color: #A0A0A0; line-height: 1.6;">
                Get a stunning portfolio, ATS-optimized resume (PDF + DOCX),
                and tailored cover letters—all in under 2 minutes.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with how_col3:
        st.markdown("""
        <div style="text-align: center; padding: 30px 20px;">
            <div style="font-size: 48px; margin-bottom: 15px;">🎯</div>
            <h3 style="color: #0070F3; margin-bottom: 10px;">3. Land Your Dream Job</h3>
            <p style="color: #A0A0A0; line-height: 1.6;">
                Download everything instantly. Optimize for specific jobs.
                Stand out from the competition with pro-level materials.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Features showcase
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## ✨ Complete Career Toolkit")
    st.markdown("<br>", unsafe_allow_html=True)

    # Row 1: Core Assets
    feat1, feat2, feat3 = st.columns(3)

    with feat1:
        st.markdown("""
        <div style="padding: 20px; text-align: center;">
            <div style="font-size: 42px; margin-bottom: 10px;">🎨</div>
            <h4 style="color: #ffffff; margin-bottom: 8px;">Portfolio Website</h4>
            <p style="color: #A0A0A0; font-size: 14px; line-height: 1.5;">
                Stunning, responsive portfolio with Framer-inspired design and instant HTML download
            </p>
        </div>
        """, unsafe_allow_html=True)

    with feat2:
        st.markdown("""
        <div style="padding: 20px; text-align: center;">
            <div style="font-size: 42px; margin-bottom: 10px;">📄</div>
            <h4 style="color: #ffffff; margin-bottom: 8px;">ATS-Optimized Resume</h4>
            <p style="color: #A0A0A0; font-size: 14px; line-height: 1.5;">
                Professional PDF + DOCX formats ready for any applicant tracking system
            </p>
        </div>
        """, unsafe_allow_html=True)

    with feat3:
        st.markdown("""
        <div style="padding: 20px; text-align: center;">
            <div style="font-size: 42px; margin-bottom: 10px;">✉️</div>
            <h4 style="color: #ffffff; margin-bottom: 8px;">Smart Cover Letters</h4>
            <p style="color: #A0A0A0; font-size: 14px; line-height: 1.5;">
                AI-tailored letters in 3 tones (formal, friendly, technical) with PDF/DOCX/TXT export
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: AI-Powered Features
    feat4, feat5, feat6 = st.columns(3)

    with feat4:
        st.markdown("""
        <div style="padding: 20px; text-align: center;">
            <div style="font-size: 42px; margin-bottom: 10px;">🎯</div>
            <h4 style="color: #ffffff; margin-bottom: 8px;">Resume Optimizer</h4>
            <p style="color: #A0A0A0; font-size: 14px; line-height: 1.5;">
                ATS score analysis with keyword matching, gap identification, and improvement tips
            </p>
        </div>
        """, unsafe_allow_html=True)

    with feat5:
        st.markdown("""
        <div style="padding: 20px; text-align: center;">
            <div style="font-size: 42px; margin-bottom: 10px;">🎤</div>
            <h4 style="color: #ffffff; margin-bottom: 8px;">Mock Interviews</h4>
            <p style="color: #A0A0A0; font-size: 14px; line-height: 1.5;">
                AI-generated questions tailored to your profile with instant feedback on your answers
            </p>
        </div>
        """, unsafe_allow_html=True)

    with feat6:
        st.markdown("""
        <div style="padding: 20px; text-align: center;">
            <div style="font-size: 42px; margin-bottom: 10px;">💬</div>
            <h4 style="color: #ffffff; margin-bottom: 8px;">AI Career Coach</h4>
            <p style="color: #A0A0A0; font-size: 14px; line-height: 1.5;">
                Interactive chatbot for career advice, salary tips, skill gaps, and job search strategy
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Stats section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## 📊 By The Numbers")
    st.markdown("<br>", unsafe_allow_html=True)

    stat1, stat2, stat3, stat4 = st.columns(4)

    with stat1:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 42px; font-weight: bold; background: linear-gradient(135deg, #FF0080, #7928CA); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">< 2 min</div>
            <p style="color: #A0A0A0; margin-top: 8px;">Complete Generation</p>
        </div>
        """, unsafe_allow_html=True)

    with stat2:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 42px; font-weight: bold; background: linear-gradient(135deg, #7928CA, #0070F3); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">6+</div>
            <p style="color: #A0A0A0; margin-top: 8px;">AI-Powered Tools</p>
        </div>
        """, unsafe_allow_html=True)

    with stat3:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 42px; font-weight: bold; background: linear-gradient(135deg, #0070F3, #00DFD8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">10+</div>
            <p style="color: #A0A0A0; margin-top: 8px;">File Formats</p>
        </div>
        """, unsafe_allow_html=True)

    with stat4:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 42px; font-weight: bold; background: linear-gradient(135deg, #FF0080, #0070F3); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">∞</div>
            <p style="color: #A0A0A0; margin-top: 8px;">Interview Questions</p>
        </div>
        """, unsafe_allow_html=True)

    # AI Features callout
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, rgba(255,0,128,0.1), rgba(121,40,202,0.1), rgba(0,112,243,0.1)); border-radius: 16px; border: 1px solid rgba(255,0,128,0.3);">
        <h2 style="color: #ffffff; margin-bottom: 20px;">🤖 Powered by Advanced AI</h2>
        <p style="color: #A0A0A0; font-size: 16px; line-height: 1.8; max-width: 800px; margin: 0 auto;">
            Built with <strong style="color: #FF0080;">Groq AI (Llama 3.3 70B)</strong> for lightning-fast, intelligent responses.
            From portfolio generation to career coaching, every feature is enhanced with state-of-the-art language models
            to give you <strong style="color: #0070F3;">personalized, actionable guidance</strong> for your career journey.
        </p>
        <br>
        <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; margin-top: 20px;">
            <div>
                <div style="font-size: 32px;">⚡</div>
                <p style="color: #888; margin-top: 5px; font-size: 14px;">Ultra-Fast</p>
            </div>
            <div>
                <div style="font-size: 32px;">🎯</div>
                <p style="color: #888; margin-top: 5px; font-size: 14px;">Hyper-Accurate</p>
            </div>
            <div>
                <div style="font-size: 32px;">💡</div>
                <p style="color: #888; margin-top: 5px; font-size: 14px;">Context-Aware</p>
            </div>
            <div>
                <div style="font-size: 32px;">🚀</div>
                <p style="color: #888; margin-top: 5px; font-size: 14px;">Always Learning</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px; color: #666;">
        <p style="font-size: 14px; margin-bottom: 10px;">
            Built with <span style="color: #FF0080;">❤️</span> using Streamlit, Groq AI (Llama 3.3), and Supabase
        </p>
        <p style="font-size: 12px; color: #444;">
            PortfolioAI • AI-Powered Career Tools for Engineers • 2025
        </p>
    </div>
    """, unsafe_allow_html=True)


def process_resume_upload(uploaded_file):
    """Process uploaded resume file"""
    with st.spinner("📄 Parsing your resume..."):
        try:
            file_bytes = uploaded_file.read()
            result = resume_parser.parse_resume(file_bytes, uploaded_file.name)

            if not result['success']:
                st.error(f"❌ {result['error']}")
                return

            st.session_state.profile_data = result['profile_data']
            st.success(f"✅ Resume parsed successfully! Confidence: {result['confidence']:.0%}")
            generate_assets()

        except Exception as e:
            st.error(f"❌ Error processing resume: {str(e)}")


def process_linkedin_input(input_text):
    """Process LinkedIn input - handles both URL and profile text"""
    import re

    # Check if input looks like a URL
    url_pattern = r'linkedin\.com/in/[\w-]+'
    url_match = re.search(url_pattern, input_text.lower())

    # Extract LinkedIn URL if present
    linkedin_url = ""
    if url_match:
        linkedin_url = input_text[url_match.start():url_match.end()]
        if not linkedin_url.startswith('http'):
            linkedin_url = 'https://' + linkedin_url

    # If input is ONLY a URL (short text), try scraping first
    if url_match and len(input_text.strip()) < 200:
        with st.spinner("🔗 Trying to fetch LinkedIn profile..."):
            try:
                result = linkedin_scraper.scrape_and_parse(linkedin_url)

                if result['success']:
                    st.session_state.profile_data = result['profile_data']
                    st.success(f"✅ Profile fetched successfully! Confidence: {result['confidence']:.0%}")
                    generate_assets()
                    return
                else:
                    # Scraping failed, inform user
                    st.warning(f"⚠️ {result['error']}")
                    st.info("💡 Please paste your full LinkedIn profile text instead of just the URL.")
                    return

            except Exception as e:
                st.error(f"❌ Error fetching LinkedIn: {str(e)}")
                st.info("💡 Please paste your full LinkedIn profile text instead.")
                return

    # Input contains text (not just URL), parse it directly
    with st.spinner("📝 Parsing your profile..."):
        try:
            result = linkedin_scraper.parse_manual_text(input_text, linkedin_url)

            if not result['success']:
                st.error(f"❌ {result['error']}")
                return

            st.session_state.profile_data = result['profile_data']
            st.success(f"✅ Profile parsed successfully! Confidence: {result['confidence']:.0%}")
            generate_assets()

        except Exception as e:
            st.error(f"❌ Error processing profile: {str(e)}")


def generate_assets():
    """Generate portfolio and resume from profile data"""
    if not st.session_state.profile_data:
        st.error("No profile data available")
        return

    profile_data = st.session_state.profile_data
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        # Step 1: Generate portfolio
        status_text.text("🎨 Generating your portfolio website...")
        progress_bar.progress(10)

        portfolio_result = portfolio_gen.generate_portfolio_with_fallback(profile_data)
        if portfolio_result['success']:
            st.session_state.portfolio_html = portfolio_result['html_content']
            st.session_state.subdomain = portfolio_result['subdomain']
            progress_bar.progress(40)

        # Step 2: Generate resume files
        status_text.text("📄 Creating your ATS-optimized resume...")
        progress_bar.progress(50)

        resume_result = resume_gen.generate_resume_files(profile_data)
        if resume_result['success']:
            st.session_state.resume_pdf = resume_result['pdf_bytes']
            st.session_state.resume_docx = resume_result['docx_bytes']
            progress_bar.progress(80)

        # Step 3: Save to database if user is logged in
        if st.session_state.user_id and not st.session_state.demo_mode:
            status_text.text("💾 Saving to your account...")
            progress_bar.progress(90)

            try:
                # Save portfolio to database (use .client to access raw client)
                supabase.client.table('user_portfolios').insert({
                    'user_id': st.session_state.user_id,
                    'profile_data': profile_data,
                    'portfolio_html': st.session_state.portfolio_html,
                    'subdomain': st.session_state.subdomain
                }).execute()

                status_text.text("✅ Portfolio saved to your account!")
            except Exception as save_error:
                st.warning(f"⚠️ Could not save to database: {str(save_error)}")

        # Complete
        status_text.text("✅ All done! Redirecting to dashboard...")
        progress_bar.progress(100)

        st.session_state.page = 'dashboard'
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error generating assets: {str(e)}")
        progress_bar.empty()
        status_text.empty()


def generate_cover_letter(job_description: str, tone: str):
    """Generate AI cover letter based on profile and job description"""
    from prompts.prompts import (
        COVER_LETTER_FORMAL_PROMPT,
        COVER_LETTER_FRIENDLY_PROMPT,
        COVER_LETTER_TECHNICAL_PROMPT
    )

    with st.spinner("✍️ Generating your cover letter..."):
        try:
            profile_data = st.session_state.profile_data

            # Select prompt based on tone
            if tone == "formal":
                system_prompt = COVER_LETTER_FORMAL_PROMPT
            elif tone == "friendly":
                system_prompt = COVER_LETTER_FRIENDLY_PROMPT
            else:  # technical
                system_prompt = COVER_LETTER_TECHNICAL_PROMPT

            # Prepare user profile summary
            profile_summary = f"""
USER PROFILE:
Name: {profile_data.get('name', 'N/A')}
Email: {profile_data.get('email', 'N/A')}

WORK EXPERIENCE:
{_format_work_history(profile_data.get('work_history', []))}

SKILLS: {', '.join(profile_data.get('skills', [])[:15])}

PROJECTS:
{_format_projects(profile_data.get('projects', []))}

JOB DESCRIPTION:
{job_description}
"""

            # Call Groq API
            response = groq_client.call_api(
                system_prompt=system_prompt,
                user_prompt=profile_summary,
                model="70b",  # Use better model for cover letters
                temperature=0.7,  # More creative
                max_tokens=800
            )

            if response.get('success'):
                cover_letter = response['content']

                # Display cover letter
                st.success("✅ Cover letter generated!")
                st.markdown("---")
                st.markdown("### Your Cover Letter")
                st.markdown(cover_letter)

                # Download buttons
                st.markdown("### ⬇️ Download Options")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.download_button(
                        label="📄 Download TXT",
                        data=cover_letter,
                        file_name=f"cover_letter_{tone}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                with col2:
                    # Generate PDF
                    from reportlab.lib.pagesizes import letter
                    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
                    from reportlab.lib.units import inch
                    from io import BytesIO

                    pdf_buffer = BytesIO()
                    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter,
                                          rightMargin=72, leftMargin=72,
                                          topMargin=72, bottomMargin=18)

                    # Container for the 'Flowable' objects
                    elements = []
                    styles = getSampleStyleSheet()

                    # Custom style for cover letter
                    letter_style = ParagraphStyle(
                        'CoverLetter',
                        parent=styles['Normal'],
                        fontSize=11,
                        leading=16,
                        spaceAfter=12
                    )

                    # Add cover letter content
                    for paragraph in cover_letter.split('\n\n'):
                        if paragraph.strip():
                            p = Paragraph(paragraph.replace('\n', '<br/>'), letter_style)
                            elements.append(p)
                            elements.append(Spacer(1, 0.1*inch))

                    doc.build(elements)
                    pdf_data = pdf_buffer.getvalue()

                    st.download_button(
                        label="📕 Download PDF",
                        data=pdf_data,
                        file_name=f"cover_letter_{tone}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                with col3:
                    # Generate DOCX
                    from docx import Document
                    from docx.shared import Pt
                    from io import BytesIO

                    docx_buffer = BytesIO()
                    document = Document()

                    # Add cover letter content
                    for paragraph in cover_letter.split('\n\n'):
                        if paragraph.strip():
                            p = document.add_paragraph(paragraph)
                            # Set font size
                            for run in p.runs:
                                run.font.size = Pt(11)

                    document.save(docx_buffer)
                    docx_data = docx_buffer.getvalue()

                    st.download_button(
                        label="📘 Download DOCX",
                        data=docx_data,
                        file_name=f"cover_letter_{tone}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
            else:
                st.error(f"❌ {response.get('error', 'Failed to generate cover letter')}")

        except Exception as e:
            st.error(f"❌ Error generating cover letter: {str(e)}")


def analyze_resume(job_description: str):
    """Analyze resume against job description for ATS optimization"""
    from prompts.prompts import OPTIMIZER_PROMPT

    with st.spinner("🔍 Analyzing your resume..."):
        try:
            profile_data = st.session_state.profile_data

            # Prepare resume summary
            resume_summary = f"""
RESUME:
Name: {profile_data.get('name', 'N/A')}

Work Experience:
{_format_work_history(profile_data.get('work_history', []))}

Skills: {', '.join(profile_data.get('skills', []))}

Projects:
{_format_projects(profile_data.get('projects', []))}

Education:
{_format_education(profile_data.get('education', []))}

JOB DESCRIPTION:
{job_description}
"""

            # Call Groq API
            result = groq_client.call_api_json(
                system_prompt=OPTIMIZER_PROMPT,
                user_prompt=resume_summary,
                model="70b",  # Use better model for analysis
                temperature=0.3,
                max_tokens=1500
            )

            if result:
                # Display results
                st.success("✅ Analysis complete!")
                st.markdown("---")

                # Score
                col1, col2 = st.columns([1, 2])

                with col1:
                    score = result.get('score', 0)
                    score_color = "#00ff00" if score >= 80 else "#ff9500" if score >= 60 else "#ff0000"
                    st.markdown(f"""
                    <div style="text-align: center; padding: 30px; background: rgba(20, 20, 25, 0.8); border-radius: 20px;">
                        <div style="font-size: 48px; font-weight: bold; color: {score_color};">{score}/100</div>
                        <p style="color: #A0A0A0; margin-top: 10px;">ATS Score</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    # Strengths
                    st.markdown("**✅ Strengths:**")
                    for strength in result.get('strengths', [])[:3]:
                        st.markdown(f"- {strength}")

                st.markdown("---")

                # Missing keywords
                st.markdown("**🔑 Missing Keywords:**")
                missing = result.get('missing_keywords', [])
                if missing:
                    keyword_html = " ".join([f'<span style="display: inline-block; background: linear-gradient(135deg, #FF0080, #0070F3); padding: 6px 12px; border-radius: 16px; margin: 4px; font-size: 14px;">{kw}</span>' for kw in missing[:10]])
                    st.markdown(keyword_html, unsafe_allow_html=True)
                else:
                    st.info("Great! You have all the key keywords.")

                st.markdown("---")

                # Suggestions
                st.markdown("**💡 Recommendations:**")
                for suggestion in result.get('suggestions', [])[:5]:
                    section = suggestion.get('section', 'General')
                    recommendation = suggestion.get('recommendation', '')
                    st.markdown(f"**{section}:** {recommendation}")

            else:
                st.error("❌ Failed to analyze resume")

        except Exception as e:
            st.error(f"❌ Error analyzing resume: {str(e)}")


def _format_work_history(work_history: list) -> str:
    """Helper to format work history for prompts"""
    if not work_history:
        return "No work experience listed"

    formatted = []
    for job in work_history[:3]:  # Limit to 3 most recent
        title = job.get('title', 'Unknown')
        company = job.get('company', 'Unknown')
        dates = job.get('dates', 'N/A')
        bullets = job.get('bullets', [])

        formatted.append(f"- {title} at {company} ({dates})")
        for bullet in bullets[:2]:  # Limit bullets
            formatted.append(f"  • {bullet}")

    return "\n".join(formatted)


def _format_projects(projects: list) -> str:
    """Helper to format projects for prompts"""
    if not projects:
        return "No projects listed"

    formatted = []
    for project in projects[:3]:  # Limit to 3 projects
        name = project.get('name', 'Unnamed Project')
        description = project.get('description', 'No description')
        techs = project.get('technologies', [])

        formatted.append(f"- {name}: {description}")
        if techs:
            formatted.append(f"  Technologies: {', '.join(techs[:5])}")

    return "\n".join(formatted)


def _format_education(education: list) -> str:
    """Helper to format education for prompts"""
    if not education:
        return "No education listed"

    formatted = []
    for edu in education:
        degree = edu.get('degree', 'Degree')
        institution = edu.get('institution', 'Institution')
        year = edu.get('year', 'N/A')
        formatted.append(f"- {degree}, {institution} ({year})")

    return "\n".join(formatted)


# ==================== DASHBOARD ====================

def dashboard_page():
    """Dashboard showing generated assets"""

    # Demo mode banner
    if st.session_state.demo_mode:
        st.warning("⚠️ **Demo Mode Active** - Your work won't be saved. Sign up to keep your portfolio!")
        col_demo1, col_demo2 = st.columns([3, 1])
        with col_demo2:
            if st.button("✨ Sign Up to Save", use_container_width=True, type="primary"):
                st.session_state.page = 'signup'
                st.rerun()

    # Header
    col1, col2 = st.columns([3, 1])

    with col1:
        name = st.session_state.profile_data.get('name', 'User') if st.session_state.profile_data else 'User'
        st.markdown(f"# 👋 Welcome, {name}!")
        if st.session_state.user_email:
            st.markdown(f"<p style='color: #888;'>{st.session_state.user_email}</p>", unsafe_allow_html=True)

    with col2:
        if st.session_state.user_id:
            if st.button("📁 My Portfolios", use_container_width=True):
                st.session_state.page = 'my_portfolios'
                st.rerun()
        if st.button("🔙 Start Over", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = 'landing'
            st.rerun()

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "✉️ Cover Letter", "🎯 Optimizer", "🎤 Mock Interview", "💬 Career Coach"])

    with tab1:
        overview_tab()
    with tab2:
        cover_letter_tab()
    with tab3:
        optimizer_tab()
    with tab4:
        mock_interview_tab()
    with tab5:
        career_coach_tab()

    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px; color: #666;">
        <p style="font-size: 14px; margin-bottom: 10px;">
            Built with <span style="color: #FF0080;">❤️</span> using Streamlit, Groq AI (Llama 3.3), and Supabase
        </p>
        <p style="font-size: 12px; color: #444;">
            PortfolioAI • AI-Powered Career Tools for Engineers • 2025
        </p>
    </div>
    """, unsafe_allow_html=True)


def regenerate_portfolio():
    """Regenerate portfolio HTML with selected model"""
    if not st.session_state.profile_data:
        st.error("⚠️ No profile data found.")
        return

    with st.spinner(f"🎨 Regenerating portfolio with {st.session_state.selected_model.upper()} model..."):
        try:
            profile_data = st.session_state.profile_data

            # Regenerate portfolio HTML
            portfolio_result = portfolio_gen.generate_portfolio_with_fallback(profile_data)

            if portfolio_result['success']:
                st.session_state.portfolio_html = portfolio_result['html_content']

                # Save to database if logged in
                if st.session_state.user_id and not st.session_state.demo_mode:
                    try:
                        supabase.client.table('user_portfolios').insert({
                            'user_id': st.session_state.user_id,
                            'profile_data': profile_data,
                            'portfolio_html': portfolio_result['html_content'],
                            'subdomain': st.session_state.subdomain
                        }).execute()
                    except Exception as e:
                        st.warning(f"⚠️ Could not save to database: {str(e)}")

                st.success(f"✅ Portfolio regenerated with {st.session_state.selected_model.upper()} model!")
                st.rerun()
            else:
                st.error(f"❌ Failed to regenerate portfolio: {portfolio_result.get('error', 'Unknown error')}")

        except Exception as e:
            st.error(f"❌ Error regenerating portfolio: {str(e)}")


def overview_tab():
    """Overview tab in dashboard"""

    # Model selector and regenerate button at the top
    st.markdown("### ⚙️ AI Model Settings")
    model_col1, model_col2 = st.columns([3, 1])

    with model_col1:
        selected_model = st.selectbox(
            "Select AI Model",
            options=['8b', '70b', 'mixtral'],
            format_func=lambda x: {
                '8b': '⚡ Llama 3.1 8B (Fast)',
                '70b': '🧠 Llama 3.3 70B (Best Quality)',
                'mixtral': '🔀 Mixtral 8x7B (Balanced)'
            }[x],
            index=['8b', '70b', 'mixtral'].index(st.session_state.selected_model),
            help="Choose the AI model for generation. 70B offers best quality, 8B is fastest."
        )
        st.session_state.selected_model = selected_model

    with model_col2:
        if st.button("🔄 Regenerate Portfolio", use_container_width=True, type="primary"):
            regenerate_portfolio()

    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🎨 Your Portfolio")

        if st.session_state.portfolio_html:
            # Portfolio preview with iframe
            with st.expander("👁️ Preview Portfolio", expanded=True):
                st.components.v1.html(st.session_state.portfolio_html, height=600, scrolling=True)

            st.download_button(
                label="⬇️ Download Portfolio HTML",
                data=st.session_state.portfolio_html,
                file_name="portfolio.html",
                mime="text/html",
                use_container_width=True
            )

            subdomain = st.session_state.subdomain or "your-portfolio"
            st.info(f"💡 **Subdomain:** `{subdomain}.portfolioai.app` (will be live after deployment)")
        else:
            st.warning("Portfolio not generated yet")

        st.markdown("---")
        st.markdown("### 📄 Your Resume")

        dl_col1, dl_col2 = st.columns(2)

        with dl_col1:
            if st.session_state.resume_pdf:
                st.download_button(
                    label="⬇️ Download PDF",
                    data=st.session_state.resume_pdf,
                    file_name="resume.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.button("⬇️ Download PDF", disabled=True, use_container_width=True)

        with dl_col2:
            if st.session_state.resume_docx:
                st.download_button(
                    label="⬇️ Download DOCX",
                    data=st.session_state.resume_docx,
                    file_name="resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            else:
                st.button("⬇️ Download DOCX", disabled=True, use_container_width=True)

    with col2:
        st.markdown("### 📊 Quick Stats")

        if st.session_state.profile_data:
            profile = st.session_state.profile_data
            st.metric("Work Experience", len(profile.get('work_history', [])))
            st.metric("Skills", len(profile.get('skills', [])))
            st.metric("Projects", len(profile.get('projects', [])))
            st.metric("Education", len(profile.get('education', [])))

            confidence = profile.get('parsing_confidence', 0)
            if confidence:
                st.markdown(f"""
                <div class="score-badge">{confidence:.0%}</div>
                <p style="text-align:center; color:#94a3b8; font-size:14px;">Parsing Confidence</p>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🚀 Pro Tip")
        st.info("💡 Check out the **Mock Interview** and **Career Coach** tabs for AI-powered career guidance!")


def cover_letter_tab():
    """Cover letter generation tab"""
    st.markdown("### ✉️ AI Cover Letter Writer")
    st.markdown("Generate a tailored cover letter for any job posting.")

    job_description = st.text_area(
        "Paste the job description",
        height=200,
        placeholder="Copy and paste the full job description here...",
        key="cover_letter_job_desc"
    )

    tone = st.selectbox(
        "Select tone",
        ["formal", "friendly", "technical"],
        help="Formal: Corporate, Friendly: Startup, Technical: Engineer-to-engineer"
    )

    if st.button("✍️ Generate Cover Letter", use_container_width=True):
        if not job_description or len(job_description) < 50:
            st.warning("⚠️ Please paste a job description (at least 50 characters)")
        elif not st.session_state.profile_data:
            st.error("⚠️ No profile data found. Please generate your portfolio first.")
        else:
            generate_cover_letter(job_description, tone)


def optimizer_tab():
    """Resume optimizer tab"""
    st.markdown("### 🎯 Resume Optimizer")
    st.markdown("Analyze your resume against a target job description.")

    job_description = st.text_area(
        "Paste target job description",
        height=200,
        placeholder="Copy and paste the job description you're targeting...",
        key="optimizer_job_desc"
    )

    if st.button("🔍 Analyze", use_container_width=True):
        if not job_description or len(job_description) < 50:
            st.warning("⚠️ Please paste a job description (at least 50 characters)")
        elif not st.session_state.profile_data:
            st.error("⚠️ No profile data found. Please generate your portfolio first.")
        else:
            analyze_resume(job_description)


def mock_interview_tab():
    """Mock interview practice tab"""
    st.markdown("### 🎤 AI Mock Interview")
    st.markdown("Practice answering common interview questions tailored to your profile.")

    if not st.session_state.profile_data:
        st.warning("⚠️ Please generate your portfolio first to get personalized questions.")
        return

    # Interview type selection
    interview_type = st.selectbox(
        "Select interview type",
        ["Technical", "Behavioral", "System Design", "Mixed"],
        help="Choose the type of interview questions you want to practice"
    )

    num_questions = st.slider("Number of questions", 3, 10, 5)

    if st.button("🎯 Generate Interview Questions", use_container_width=True):
        with st.spinner("Generating personalized interview questions..."):
            try:
                profile = st.session_state.profile_data

                # Build profile summary
                profile_summary = f"""
Name: {profile.get('name', 'N/A')}
Title: {profile.get('title', 'N/A')}
Skills: {', '.join(profile.get('skills', [])[:10])}
Experience: {len(profile.get('work_history', []))} positions
Projects: {len(profile.get('projects', []))} projects
"""

                prompt = f"""You are an expert technical interviewer. Generate {num_questions} {interview_type.lower()} interview questions for this candidate.

Candidate Profile:
{profile_summary}

Generate questions that are:
1. Relevant to their skills and experience level
2. Progressively challenging
3. Realistic for actual interviews
4. Specific to their background

For each question, provide:
- The question
- Key points to cover in an ideal answer
- Common mistakes to avoid

Return as JSON array with format:
[{{"question": "...", "key_points": ["...", "..."], "mistakes": ["...", "..."]}}]
"""

                response = groq_client.call_api(
                    system_prompt="You are an expert technical interviewer.",
                    user_prompt=prompt,
                    model="70b",
                    response_format={"type": "json_object"}
                )

                if response.get('success'):
                    import json
                    try:
                        parsed_data = json.loads(response['content'])

                        # Handle different response structures
                        if isinstance(parsed_data, list):
                            questions = parsed_data
                        elif isinstance(parsed_data, dict):
                            # If it's a dict, try to find the questions array
                            questions = parsed_data.get('questions', [])
                            if not questions:
                                # Try other common keys
                                questions = parsed_data.get('data', [])
                                if not questions:
                                    # If still no questions, wrap the dict itself
                                    questions = [parsed_data]
                        else:
                            st.error("Unexpected response format")
                            questions = []

                        if not questions:
                            st.error("No questions generated. Please try again.")
                        else:
                            st.session_state.mock_interview_questions = questions
                            st.success(f"✅ Generated {len(questions)} questions!")

                            # Display questions
                            for i, q in enumerate(questions, 1):
                                if not isinstance(q, dict):
                                    st.warning(f"Question {i} has invalid format, skipping...")
                                    continue

                                question_text = q.get('question', 'Question not available')
                                preview = question_text[:80] + "..." if len(question_text) > 80 else question_text

                                with st.expander(f"❓ Question {i}: {preview}"):
                                    st.markdown(f"**Question:** {question_text}")
                                    st.markdown("**Key Points to Cover:**")
                                    for point in q.get('key_points', []):
                                        st.markdown(f"- {point}")
                                    st.markdown("**Common Mistakes to Avoid:**")
                                    for mistake in q.get('mistakes', []):
                                        st.markdown(f"- {mistake}")

                                    # Answer practice area
                                    st.markdown("---")
                                    st.markdown("**Your Answer:**")
                                    answer = st.text_area(
                                        "Practice your answer here",
                                        height=150,
                                        key=f"answer_{i}",
                                        placeholder="Write or practice your answer..."
                                    )

                                    if answer and st.button(f"Get Feedback", key=f"feedback_{i}"):
                                        feedback_prompt = f"""You are an interview coach. Review this answer to the interview question.

Question: {question_text}

Candidate's Answer: {answer}

Provide constructive feedback on:
1. Strengths of the answer
2. Areas for improvement
3. Missing key points
4. Overall rating (1-5 stars)

Be encouraging but honest."""

                                        with st.spinner("Analyzing your answer..."):
                                            feedback_response = groq_client.call_api(
                                                system_prompt="You are an interview coach.",
                                                user_prompt=feedback_prompt,
                                                model="70b"
                                            )
                                            if feedback_response.get('success'):
                                                st.markdown("**💡 Feedback:**")
                                                st.info(feedback_response['content'])
                    except json.JSONDecodeError as e:
                        st.error(f"Failed to parse response: {str(e)}")
                    except Exception as e:
                        st.error(f"Error processing questions: {str(e)}")
                else:
                    st.error("Failed to generate questions. Please try again.")

            except Exception as e:
                st.error(f"Error generating questions: {str(e)}")

    # Show previously generated questions
    elif st.session_state.mock_interview_questions:
        st.info(f"📝 You have {len(st.session_state.mock_interview_questions)} questions ready. Click 'Generate' to create new ones.")


def career_coach_tab():
    """AI Career Coach tab with chatbot interface"""
    st.markdown("### 💬 AI Career Coach")
    st.markdown("Chat with your personal AI career advisor for guidance and support.")

    if not st.session_state.profile_data:
        st.warning("⚠️ Please generate your portfolio first to get personalized advice.")
        return

    # Build profile context once
    profile = st.session_state.profile_data
    profile_context = f"""
Candidate Profile:
- Name: {profile.get('name', 'N/A')}
- Current Title: {profile.get('title', 'N/A')}
- Years of Experience: ~{len(profile.get('work_history', []))} positions
- Core Skills: {', '.join(profile.get('skills', [])[:15])}
- Projects: {len(profile.get('projects', []))} projects
- Education: {len(profile.get('education', []))} degrees/certifications
"""

    # Mode toggle and controls
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        mode = st.radio(
            "Mode",
            ["💬 Chat", "🎯 Quick Topics"],
            horizontal=True,
            key="coach_mode_radio"
        )
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.career_coach_chat_history = []
            st.rerun()
    with col3:
        if st.button("📋 Export Chat", use_container_width=True):
            if st.session_state.career_coach_chat_history:
                chat_export = "\n\n".join([
                    f"{'You' if msg['role'] == 'user' else 'Coach'}: {msg['content']}"
                    for msg in st.session_state.career_coach_chat_history
                ])
                st.download_button(
                    label="⬇️ Download",
                    data=chat_export,
                    file_name="career_coach_chat.txt",
                    mime="text/plain"
                )

    st.markdown("---")

    if mode == "💬 Chat":
        # Chat interface
        st.markdown("#### 💭 Chat with Your Career Coach")

        # Display starter prompts if no chat history
        if not st.session_state.career_coach_chat_history:
            st.markdown("**💡 Suggested Topics to Get Started:**")
            starter_col1, starter_col2, starter_col3 = st.columns(3)

            starters = [
                "What career paths should I consider?",
                "How can I improve my skills?",
                "Tips for salary negotiation?",
                "How to build my personal brand?",
                "Job search strategies for me?",
                "Work-life balance advice?"
            ]

            for i, starter in enumerate(starters):
                col = [starter_col1, starter_col2, starter_col3][i % 3]
                with col:
                    if st.button(starter, key=f"starter_{i}", use_container_width=True):
                        # Add user message to history
                        st.session_state.career_coach_chat_history.append({
                            "role": "user",
                            "content": starter
                        })

                        # Get AI response
                        with st.spinner("🤔 Thinking..."):
                            response = get_career_coach_response(starter, profile_context)

                        if response:
                            st.session_state.career_coach_chat_history.append({
                                "role": "assistant",
                                "content": response
                            })

                        st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

        # Display chat history
        if st.session_state.career_coach_chat_history:
            st.markdown("### 💬 Conversation")

            # Chat container with styling
            for i, message in enumerate(st.session_state.career_coach_chat_history):
                if message["role"] == "user":
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(255,0,128,0.1), rgba(121,40,202,0.1));
                                border-left: 3px solid #FF0080; padding: 15px; border-radius: 8px; margin: 10px 0;">
                        <strong>You:</strong><br>{message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.05);
                                border-left: 3px solid #0070F3; padding: 15px; border-radius: 8px; margin: 10px 0;">
                        <strong>Career Coach:</strong><br>{message['content']}
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

        # Chat input
        user_message = st.text_area(
            "Your message",
            height=100,
            placeholder="Ask anything about your career, job search, skills, salary, or professional development...",
            key="career_coach_input"
        )

        if st.button("📤 Send Message", use_container_width=True, type="primary"):
            if not user_message or len(user_message.strip()) < 3:
                st.warning("⚠️ Please enter a message.")
            else:
                # Add user message
                st.session_state.career_coach_chat_history.append({
                    "role": "user",
                    "content": user_message
                })

                # Get AI response
                with st.spinner("🤔 Career coach is thinking..."):
                    response = get_career_coach_response(user_message, profile_context)

                if response:
                    st.session_state.career_coach_chat_history.append({
                        "role": "assistant",
                        "content": response
                    })
                    st.rerun()
                else:
                    st.error("Failed to get response. Please try again.")

    else:
        # Quick Topics mode (original functionality)
        st.markdown("#### 🎯 Quick Career Topics")
        st.markdown("Select a topic for instant, focused advice.")

        coaching_topic = st.selectbox(
            "What would you like help with?",
            [
                "Career Path Recommendations",
                "Skill Gap Analysis",
                "Salary Negotiation Tips",
                "Job Search Strategy",
                "Personal Branding",
                "Work-Life Balance",
                "Career Transition Advice"
            ]
        )

        if st.button("💡 Get Instant Advice", use_container_width=True, type="primary"):
            with st.spinner("Generating personalized advice..."):
                topic_prompts = {
                    "Career Path Recommendations": "Based on their profile, suggest 3-4 potential career paths with why it's a good fit, skills they already have, skills to develop, typical timeline, and salary expectations.",
                    "Skill Gap Analysis": "Analyze their current skillset and identify top 5 in-demand skills they should learn, skills they have that are highly valuable, technologies that are becoming obsolete, and learning resources for each skill gap.",
                    "Salary Negotiation Tips": "Provide salary negotiation advice including market rate for their experience level, how to research salary data, negotiation scripts and tactics, common mistakes to avoid, and when to negotiate.",
                    "Job Search Strategy": "Create a personalized job search plan with best job boards and platforms for their profile, how to optimize their application process, networking strategies, companies that match their background, and timeline and goals.",
                    "Personal Branding": "Help them build their personal brand with unique value proposition, content creation strategy, social media optimization, portfolio/blog ideas, and community engagement.",
                    "Work-Life Balance": "Advice on maintaining work-life balance including time management strategies, setting boundaries, productivity techniques, avoiding burnout, and career vs personal life priorities.",
                    "Career Transition Advice": "Guide them through a career transition with transferable skills analysis, positioning for new roles, learning roadmap, networking in new field, and resume/portfolio adjustments."
                }

                prompt = f"""{profile_context}

Topic: {coaching_topic}

{topic_prompts[coaching_topic]}

Provide comprehensive, actionable advice tailored to their specific situation. Be encouraging but realistic."""

                response = get_career_coach_response(prompt, profile_context, use_full_prompt=True)

                if response:
                    st.markdown("### 💡 Your Personalized Career Advice")
                    st.markdown("---")
                    st.markdown(response)
                    st.markdown("---")
                    st.info("💡 Switch to **Chat Mode** for follow-up questions and deeper discussion!")
                else:
                    st.error("Failed to generate advice. Please try again.")


def get_career_coach_response(user_message: str, profile_context: str, use_full_prompt: bool = False) -> str:
    """Get response from career coach AI with conversation context"""
    try:
        # Build conversation history for context
        conversation_context = ""
        if st.session_state.career_coach_chat_history and not use_full_prompt:
            # Include last 3 exchanges for context
            recent_history = st.session_state.career_coach_chat_history[-6:]
            conversation_context = "\n\nPrevious conversation:\n"
            for msg in recent_history:
                role = "User" if msg["role"] == "user" else "Coach"
                conversation_context += f"{role}: {msg['content']}\n"

        system_prompt = """You are an experienced career coach specializing in tech careers. You provide:
- Personalized, actionable career advice
- Honest and realistic guidance
- Encouraging and supportive feedback
- Specific next steps and resources
- Industry insights and trends

Keep responses conversational, concise (2-3 paragraphs unless asked for more detail), and focused on practical advice."""

        if use_full_prompt:
            user_prompt = user_message
        else:
            user_prompt = f"""{profile_context}

{conversation_context}

Current question: {user_message}

Provide helpful, specific advice based on their profile and conversation context."""

        response = groq_client.call_api(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model="70b",
            temperature=0.7
        )

        if response.get('success'):
            return response['content']
        else:
            return None

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


# ==================== Q&A FLOW PAGE ====================

def qa_flow_page():
    """Q&A flow for users without resume"""
    st.markdown("""
    <div class="hero">
        <h1 class="gradient-text">Build Your Profile</h1>
        <p>Answer a few questions to create your AI-powered portfolio</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Progress indicator
    progress_text = st.empty()
    progress_bar = st.progress(0)

    # Step-by-step form
    with st.form("qa_form"):
        st.markdown("### 👤 Personal Information")
        name = st.text_input("Full Name *", placeholder="John Doe")
        title = st.text_input("Professional Title *", placeholder="Full Stack Developer")
        email = st.text_input("Email", placeholder="john@example.com")
        phone = st.text_input("Phone", placeholder="+1 (555) 123-4567")
        location = st.text_input("Location", placeholder="San Francisco, CA")

        st.markdown("---")
        st.markdown("### 💼 Professional Summary")
        summary = st.text_area(
            "Tell us about yourself *",
            height=120,
            placeholder="Brief professional summary (2-3 sentences)..."
        )

        st.markdown("---")
        st.markdown("### 💻 Skills")
        skills_input = st.text_area(
            "List your technical skills *",
            height=100,
            placeholder="Python, JavaScript, React, Node.js, AWS, Docker... (comma-separated)"
        )

        st.markdown("---")
        st.markdown("### 💼 Work Experience")
        st.markdown("Add at least one work experience")

        num_jobs = st.number_input("Number of positions to add", min_value=1, max_value=5, value=1)

        work_history = []
        for i in range(int(num_jobs)):
            st.markdown(f"**Position {i+1}**")
            col1, col2 = st.columns(2)
            with col1:
                job_title = st.text_input(f"Job Title {i+1} *", key=f"job_title_{i}", placeholder="Software Engineer")
                company = st.text_input(f"Company {i+1} *", key=f"company_{i}", placeholder="Tech Corp")
            with col2:
                start_date = st.text_input(f"Start Date {i+1}", key=f"start_{i}", placeholder="Jan 2020")
                end_date = st.text_input(f"End Date {i+1}", key=f"end_{i}", placeholder="Present")

            responsibilities = st.text_area(
                f"Key responsibilities and achievements {i+1}",
                height=100,
                key=f"resp_{i}",
                placeholder="- Built and deployed web applications\n- Led team of 3 developers\n- Improved performance by 40%"
            )

            if job_title and company:
                work_history.append({
                    'title': job_title,
                    'company': company,
                    'start_date': start_date,
                    'end_date': end_date,
                    'responsibilities': responsibilities.split('\n') if responsibilities else []
                })

        st.markdown("---")
        st.markdown("### 🚀 Projects")
        st.markdown("Add your notable projects (optional)")

        num_projects = st.number_input("Number of projects to add", min_value=0, max_value=5, value=1)

        projects = []
        for i in range(int(num_projects)):
            st.markdown(f"**Project {i+1}**")
            col1, col2 = st.columns(2)
            with col1:
                project_name = st.text_input(f"Project Name {i+1}", key=f"proj_name_{i}", placeholder="E-commerce Platform")
            with col2:
                project_url = st.text_input(f"URL/GitHub {i+1}", key=f"proj_url_{i}", placeholder="https://github.com/...")

            project_desc = st.text_area(
                f"Project description {i+1}",
                height=80,
                key=f"proj_desc_{i}",
                placeholder="Built a full-stack e-commerce platform with React and Node.js..."
            )

            project_tech = st.text_input(
                f"Technologies used {i+1}",
                key=f"proj_tech_{i}",
                placeholder="React, Node.js, MongoDB"
            )

            if project_name:
                projects.append({
                    'name': project_name,
                    'url': project_url,
                    'description': project_desc,
                    'technologies': [t.strip() for t in project_tech.split(',')] if project_tech else []
                })

        st.markdown("---")
        st.markdown("### 🎓 Education")
        num_edu = st.number_input("Number of degrees/certifications", min_value=1, max_value=5, value=1)

        education = []
        for i in range(int(num_edu)):
            st.markdown(f"**Education {i+1}**")
            col1, col2, col3 = st.columns(3)
            with col1:
                degree = st.text_input(f"Degree {i+1} *", key=f"degree_{i}", placeholder="B.S. Computer Science")
            with col2:
                institution = st.text_input(f"Institution {i+1} *", key=f"institution_{i}", placeholder="MIT")
            with col3:
                year = st.text_input(f"Year {i+1}", key=f"year_{i}", placeholder="2020")

            if degree and institution:
                education.append({
                    'degree': degree,
                    'institution': institution,
                    'year': year
                })

        st.markdown("---")
        st.markdown("### 🔗 Links (Optional)")
        col1, col2 = st.columns(2)
        with col1:
            github = st.text_input("GitHub", placeholder="https://github.com/username")
            linkedin_url = st.text_input("LinkedIn", placeholder="https://linkedin.com/in/username")
        with col2:
            portfolio_url = st.text_input("Portfolio Website", placeholder="https://yoursite.com")
            twitter = st.text_input("Twitter/X", placeholder="https://twitter.com/username")

        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("🎨 Generate My Portfolio", use_container_width=True, type="primary")

    if submit:
        # Validation
        if not name or not title or not summary or not skills_input or len(work_history) == 0 or len(education) == 0:
            st.error("⚠️ Please fill in all required fields (*)")
        elif len(summary) < 20:
            st.error("⚠️ Professional summary should be at least 20 characters")
        else:
            progress_text.text("✨ Building your profile...")
            progress_bar.progress(20)

            # Build profile data structure
            profile_data = {
                'name': name,
                'title': title,
                'email': email,
                'phone': phone,
                'location': location,
                'summary': summary,
                'skills': [s.strip() for s in skills_input.split(',')],
                'work_history': work_history,
                'projects': projects,
                'education': education,
                'links': {
                    'github': github,
                    'linkedin': linkedin_url,
                    'portfolio': portfolio_url,
                    'twitter': twitter
                },
                'parsing_confidence': 1.0  # Manual entry is 100% confident
            }

            st.session_state.profile_data = profile_data
            st.session_state.qa_data = profile_data

            # Generate subdomain
            subdomain = name.lower().replace(' ', '-').replace('.', '')
            st.session_state.subdomain = subdomain

            progress_text.text("🎨 Generating portfolio HTML...")
            progress_bar.progress(40)

            # Generate portfolio
            portfolio_result = portfolio_gen.generate_portfolio_with_fallback(profile_data)
            if portfolio_result['success']:
                st.session_state.portfolio_html = portfolio_result['html_content']
            else:
                st.error(f"Failed to generate portfolio: {portfolio_result.get('error', 'Unknown error')}")
                return

            progress_text.text("📄 Creating resume PDF...")
            progress_bar.progress(60)

            # Generate resume
            success_pdf, resume_pdf, error_pdf = resume_gen.generate_pdf(profile_data)
            if success_pdf:
                st.session_state.resume_pdf = resume_pdf
            else:
                st.error(f"Failed to generate PDF: {error_pdf}")

            progress_text.text("📝 Creating resume DOCX...")
            progress_bar.progress(80)

            success_docx, resume_docx, error_docx = resume_gen.generate_docx(profile_data)
            if success_docx:
                st.session_state.resume_docx = resume_docx
            else:
                st.error(f"Failed to generate DOCX: {error_docx}")

            # Save to database if logged in
            if st.session_state.user_id and not st.session_state.demo_mode:
                progress_text.text("💾 Saving to your account...")
                progress_bar.progress(90)

                try:
                    supabase.client.table('user_portfolios').insert({
                        'user_id': st.session_state.user_id,
                        'profile_data': profile_data,
                        'portfolio_html': st.session_state.portfolio_html,
                        'subdomain': subdomain
                    }).execute()
                except Exception as save_error:
                    st.warning(f"⚠️ Could not save to database: {str(save_error)}")

            progress_text.text("✅ All done!")
            progress_bar.progress(100)

            time.sleep(1)

            # Navigate to dashboard
            st.session_state.page = 'dashboard'
            st.rerun()

    # Back button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 Back to Home"):
        st.session_state.page = 'landing'
        st.rerun()


# ==================== AUTH PAGES ====================

def login_page():
    """Login page"""
    st.markdown("""
    <div class="hero">
        <h1 class="gradient-text">Welcome Back</h1>
        <p>Sign in to access your saved portfolios</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("login_form"):
            st.markdown("### 🔐 Sign In")
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")

            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("Sign In", use_container_width=True, type="primary")
            with col_b:
                back = st.form_submit_button("Back", use_container_width=True)

            if submit:
                if not email or not password:
                    st.error("Please enter both email and password")
                else:
                    with st.spinner("Signing in..."):
                        try:
                            # Use wrapper's login method
                            response = supabase.login(email, password)

                            if response.get('success') and response.get('user'):
                                st.session_state.user_id = response['user'].id
                                st.session_state.user_email = response['user'].email
                                st.session_state.demo_mode = False
                                st.success("✅ Signed in successfully!")
                                st.session_state.page = 'my_portfolios'
                                st.rerun()
                            else:
                                st.error(f"Login failed: {response.get('error', 'Invalid credentials')}")
                        except Exception as e:
                            st.error(f"Login failed: {str(e)}")

            if back:
                st.session_state.page = 'landing'
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Don't have an account? <a href='#' style='color: #FF0080;'>Sign up</a></p>", unsafe_allow_html=True)

        if st.button("Create Account", use_container_width=True):
            st.session_state.page = 'signup'
            st.rerun()


def signup_page():
    """Signup page"""
    st.markdown("""
    <div class="hero">
        <h1 class="gradient-text">Get Started Free</h1>
        <p>Create an account to save your portfolios</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("signup_form"):
            st.markdown("### ✨ Sign Up")
            name = st.text_input("Full Name", placeholder="John Doe")
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password", placeholder="Min. 8 characters")
            password_confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")

            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("Create Account", use_container_width=True, type="primary")
            with col_b:
                back = st.form_submit_button("Back", use_container_width=True)

            if submit:
                if not name or not email or not password:
                    st.error("Please fill in all fields")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters")
                elif password != password_confirm:
                    st.error("Passwords don't match")
                else:
                    with st.spinner("Creating account..."):
                        try:
                            # Use wrapper's signup method
                            response = supabase.signup(email, password)

                            if response.get('success') and response.get('user'):
                                st.session_state.user_id = response['user'].id
                                st.session_state.user_email = response['user'].email
                                st.session_state.demo_mode = False
                                st.success("✅ Account created! You're signed in.")
                                st.info("💡 Check your email to verify your account")
                                st.session_state.page = 'landing'
                                st.rerun()
                            else:
                                st.error(f"Signup failed: {response.get('error', 'Failed to create account')}")
                        except Exception as e:
                            st.error(f"Signup failed: {str(e)}")

            if back:
                st.session_state.page = 'landing'
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Already have an account? <a href='#' style='color: #FF0080;'>Sign in</a></p>", unsafe_allow_html=True)

        if st.button("Sign In Instead", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()


def my_portfolios_page():
    """My Portfolios page for logged-in users"""
    # Header
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f"# 📁 My Portfolios")
        if st.session_state.user_email:
            st.markdown(f"<p style='color: #888;'>{st.session_state.user_email}</p>", unsafe_allow_html=True)

    with col2:
        if st.button("🔙 Create New", use_container_width=True, type="primary"):
            st.session_state.page = 'landing'
            st.rerun()
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.session_state.demo_mode = False
            st.session_state.page = 'landing'
            st.rerun()

    st.markdown("---")

    # Load saved portfolios from database
    if st.session_state.user_id:
        try:
            # Query Supabase for user's portfolios (use .client to access raw client)
            response = supabase.client.table('user_portfolios').select('*').eq('user_id', st.session_state.user_id).order('created_at', desc=True).execute()

            portfolios = response.data if response.data else []

            if not portfolios:
                st.info("📝 You haven't created any portfolios yet. Click 'Create New' to get started!")
            else:
                st.markdown(f"### You have {len(portfolios)} saved portfolio(s)")
                st.markdown("<br>", unsafe_allow_html=True)

                # Display portfolios in grid
                for i in range(0, len(portfolios), 2):
                    col1, col2 = st.columns(2)

                    with col1:
                        if i < len(portfolios):
                            portfolio = portfolios[i]
                            display_portfolio_card(portfolio, i)

                    with col2:
                        if i + 1 < len(portfolios):
                            portfolio = portfolios[i + 1]
                            display_portfolio_card(portfolio, i + 1)

        except Exception as e:
            st.error(f"Error loading portfolios: {str(e)}")
    else:
        st.warning("Please sign in to view your portfolios")


def display_portfolio_card(portfolio, index):
    """Display a single portfolio card"""
    st.markdown(f"""
    <div style="background: rgba(20, 20, 25, 0.8); padding: 20px; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h4 style="color: #ffffff; margin-bottom: 10px;">Portfolio #{index + 1}</h4>
        <p style="color: #888; font-size: 14px;">Created: {portfolio.get('created_at', 'N/A')[:10]}</p>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("👁️ View", key=f"view_{index}", use_container_width=True):
            # Load portfolio data into session
            st.session_state.profile_data = portfolio.get('profile_data')
            st.session_state.portfolio_html = portfolio.get('portfolio_html')
            st.session_state.page = 'dashboard'
            st.rerun()

    with col_b:
        if portfolio.get('portfolio_html'):
            st.download_button(
                "⬇️ HTML",
                data=portfolio.get('portfolio_html'),
                file_name=f"portfolio_{index+1}.html",
                mime="text/html",
                key=f"download_{index}",
                use_container_width=True
            )

    with col_c:
        if st.button("🗑️ Delete", key=f"delete_{index}", use_container_width=True):
            try:
                supabase.client.table('user_portfolios').delete().eq('id', portfolio['id']).execute()
                st.success("Deleted!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")


# ==================== MAIN ROUTING ====================

def main():
    """Main application router"""
    if st.session_state.page == 'landing':
        landing_page()
    elif st.session_state.page == 'login':
        login_page()
    elif st.session_state.page == 'signup':
        signup_page()
    elif st.session_state.page == 'my_portfolios':
        my_portfolios_page()
    elif st.session_state.page == 'qa_flow':
        qa_flow_page()
    elif st.session_state.page == 'dashboard':
        dashboard_page()
    else:
        landing_page()


if __name__ == "__main__":
    main()
