# PortfolioAI — Product Requirements Document

## CONTENTS

- Abstract
- Business Objectives
- KPI
- Success Criteria
- User Journeys
- Scenarios
- User Flow
- Functional Requirements
- Model Requirements
- Data Requirements
- Prompt Requirements
- Testing & Measurement
- Risks & Mitigations
- Costs
- Assumptions & Dependencies
- Compliance/Privacy/Legal
- GTM/Rollout Plan

---

## 📝 Abstract

**PortfolioAI** is an AI-driven web application that transforms raw career inputs (uploaded résumé, LinkedIn URL, or guided Q&A) into a complete job-readiness suite in minutes. Target users are bootcamp graduates and early-career engineers (0–2 years of experience) who lack polished online presence and struggle with creating portfolios, ATS-optimized résumés, and tailored cover letters. The product generates a fully hosted portfolio site, ATS-ready résumé, personalized job alerts, and provides AI-powered mock interviews with real-time coaching. This eliminates days of manual work and helps users apply confidently to 20+ roles.

**Rationale:** Early-career engineers face three critical barriers: (1) no professional portfolio, (2) generic application materials that fail ATS screening, and (3) ad-hoc interview preparation. PortfolioAI solves all three in a single, fast workflow.

---

## 🎯 Business Objectives

- **Accelerate job-seeker readiness** by reducing portfolio and résumé creation time from days to minutes
- **Increase application success rates** through ATS-optimized résumés and tailored cover letters
- **Build sticky engagement** via personalized job alerts and ongoing mock interview practice
- **Establish brand authority** in the early-career tech job-prep space during hackathon demo and post-launch
- **Validate product-market fit** quickly with activation and retention metrics to inform post-hackathon roadmap

---

## 📊 KPI

| GOAL                  | METRIC                   | QUESTION                                                      | TARGET (Weeks 1–12) |
| --------------------- | ------------------------ | ------------------------------------------------------------- | ------------------- |
| New User Growth       | # New Signups            | How many users discover and register for PortfolioAI          | 500+ signups        |
| Core Activation       | % Generate Portfolio + CV | What % of signups complete the core value prop (portfolio + résumé) | 70%+                |
| Early Retention       | D7 Retention             | What % return within 7 days to use additional features (mock interview, job alerts) | 50%+                |

---

## 🏆 Success Criteria

**Quantitative:**
- Achieve 70%+ core activation (portfolio + résumé generated)
- Reach 50%+ D7 retention (users return for mock interviews, job alerts, or cover letters)
- Maintain <30 second median time-to-portfolio generation

**Qualitative:**
- Win or place in hackathon demo (judges recognize vision and execution)
- Collect 20+ user testimonials or feedback responses within first 4 weeks post-launch
- Zero critical bugs during hackathon demo (auth, generation, hosting must work flawlessly)
- Positive sentiment on Product Hunt or Hacker News if soft-launched post-hackathon

---

## 🚶‍♀️ User Journeys

### Journey 1: Fresh Bootcamp Grad — Portfolio from Scratch
**Maya** just graduated from a 12-week bootcamp. She has no portfolio and her résumé is a plain Google Doc. She uploads her résumé PDF to PortfolioAI. In 20 seconds, she gets a live portfolio site (maya-portfolio.portfolioai.app) showcasing her three projects, skills, and contact info—plus a polished ATS-ready résumé. She downloads the résumé, sets up job alerts for "junior frontend React," and books a mock interview for the weekend. She returns 3 days later to generate a cover letter for a specific Stripe opening.

### Journey 2: Career-Switcher — LinkedIn to Portfolio
**James** worked 4 years in project management and just completed a part-time coding bootcamp. He pastes his LinkedIn URL into PortfolioAI. The AI extracts his PM experience, identifies transferable skills (Agile, stakeholder management), and generates a portfolio emphasizing his hybrid background. He uses the optimizer to score his résumé against a "Technical Product Manager" job description, sees a keyword gap (missing "SQL"), and clicks "auto-rewrite" to add SQL projects from his bootcamp. He completes a behavioral mock interview and gets coaching on answering "Why are you switching careers?"

### Journey 3: CS Grad — Job Alert Power User
**Li** graduated with a CS degree but has applied to 50+ jobs with no responses. She uploads her résumé and discovers her optimizer score is 42/100 for her target role. PortfolioAI suggests adding metrics and renaming vague project titles. She regenerates her résumé (now 78/100) and sets up job alerts for "new grad SWE" across LinkedIn, Wellfound, and AngelList. Every morning she gets 5 curated alerts with an "Apply-with-Profile" shortcut that auto-fills cover letters. Within 2 weeks, she lands 3 interviews.

---

## 📖 Scenarios

**Primary Scenarios:**
1. User uploads résumé → generates portfolio + résumé in <30 seconds
2. User pastes LinkedIn URL → AI scrapes and structures career data → portfolio + résumé generated
3. User has no résumé → completes guided Q&A (5–10 questions) → AI builds résumé from scratch
4. User inputs job description → gets tailored cover letter in editable tone (formal, friendly, technical)
5. User runs optimizer → sees keyword gap analysis → clicks "auto-rewrite" → updated résumé + portfolio
6. User starts mock interview → AI asks role-specific questions (frontend, backend, PM, etc.) → live transcript with confidence scoring and improvement tips
7. User sets job alert preferences → receives daily/weekly email + in-app notifications → clicks "Apply-with-Profile" to auto-generate cover letter
8. User chats with AI career coach → gets skill gap analysis and personalized learning recommendations

**Edge Scenarios:**
- User uploads résumé with non-standard formatting → AI parsing fails → fallback to guided Q&A
- User pastes private LinkedIn URL → scraping blocked → prompt to upload PDF or use Q&A
- Groq API rate limit hit during demo → show cached example or graceful error with retry button
- User tries to register with existing email → Supabase returns error → show "Account exists, please log in"

---

## 🕹️ User Flow

### Happy Path (First-Time User)

1. **Landing Page**
   - Hero: "From résumé to hired in minutes"
   - 3 input options: Upload résumé (PDF/Word), Paste LinkedIn URL, Start from scratch (Q&A)
   - No auth required to start

2. **Input & Processing**
   - User chooses input method
   - AI processing: "Analyzing your background..." (progress bar, 10–30 sec)
   - Groq AI extracts: work history, skills, projects, education, contact info

3. **Dashboard (All Assets Generated)**
   - **Top section:** Live portfolio preview + custom subdomain link (e.g., maya-dev.portfolioai.app)
   - **Download section:** ATS-ready résumé (PDF + DOCX)
   - **Optimizer card:** Portfolio/résumé score vs. target role (keyword analysis, improvement suggestions)
   - **3 Action Buttons:**
     - "Generate Cover Letter" (modal: paste job description)
     - "Start Mock Interview" (choose role: Frontend, Backend, Fullstack, PM, etc.)
     - "Set Up Job Alerts" (keywords, sources, frequency)

4. **Optional Signup Prompt**
   - "Create account to save your portfolio & get job alerts"
   - Email + password (Supabase Auth)
   - If user skips: session persists temporarily (local storage + temporary DB entry)

5. **Ongoing Use**
   - Job alerts → email + in-app notifications with "Apply-with-Profile" shortcut
   - Mock interview → transcript saved, progress tracked over time
   - Career coaching → chat interface analyzing skill gaps based on target roles
   - Return to dashboard anytime to regenerate, edit, or optimize

### Alternative Flows
- **Returning user:** Login → dashboard with saved portfolio, résumé, alerts
- **Optimizer flow:** User inputs job description → sees score + keyword gaps → clicks "Auto-rewrite" → AI updates résumé + portfolio → new score displayed
- **Mock interview flow:** User selects role type → AI generates 5–8 questions → user speaks or types answers → AI provides confidence score + improvement tips → transcript saved

---

## 🧰 Functional Requirements

### Core Features

| SECTION                         | SUB-SECTION              | USER STORY & EXPECTED BEHAVIORS                                                                                                                                                                                               | SCREENS      |
| ------------------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| **Landing & Input**             | Upload Résumé            | As a user, I can upload a PDF or Word résumé so the AI can extract my career data and generate my portfolio. **Behaviors:** File validation, max 5MB, supported formats (.pdf, .docx), progress indicator during upload.      | TBD          |
| **Landing & Input**             | LinkedIn URL             | As a user, I can paste my LinkedIn URL so the AI can scrape my profile and build my portfolio. **Behaviors:** URL validation, scraping with fallback to manual input if blocked, loading state during extraction.             | TBD          |
| **Landing & Input**             | Guided Q&A               | As a user with no résumé, I can answer 5–10 questions so the AI can build my résumé from scratch. **Behaviors:** Dynamic follow-up questions, progress indicator, ability to skip optional fields.                            | TBD          |
| **AI Portfolio Builder**        | Portfolio Generation     | As a user, I receive a fully responsive, hosted portfolio site in <30 seconds with custom subdomain and exportable HTML. **Behaviors:** Live preview, custom subdomain assignment, one-click export (HTML + CSS bundle).       | TBD          |
| **AI CV Generator**             | Résumé Generation        | As a user, I receive an ATS-optimized résumé in PDF and DOCX formats. **Behaviors:** Download buttons, formatting adheres to ATS standards (no tables/graphics in body), includes contact, work, skills, education sections.  | TBD          |
| **AI Cover-Letter Writer**      | Cover Letter Generation  | As a user, I input a job description and get a tailored cover letter in <10 seconds. **Behaviors:** Editable tone presets (formal, friendly, technical), live preview, copy-to-clipboard, download as PDF or DOCX.            | TBD          |
| **Résumé / Portfolio Optimizer** | Score & Gap Analysis     | As a user, I input a target job description and receive a score (0–100) with keyword gap analysis. **Behaviors:** Highlights missing keywords, suggests additions, compares user skills to job requirements.                  | TBD          |
| **Résumé / Portfolio Optimizer** | Auto-Rewrite             | As a user, I can click "Auto-rewrite" to let AI update my résumé and portfolio based on optimizer suggestions. **Behaviors:** New version generated, side-by-side diff view, option to accept or revert changes.              | TBD          |
| **AI Mock Interviewer**         | Role Selection           | As a user, I choose my target role (Frontend, Backend, Fullstack, PM, Data Science, etc.) to get relevant interview questions. **Behaviors:** Dropdown or card selection, role-specific question sets (5–8 questions).        | TBD          |
| **AI Mock Interviewer**         | Interview Session        | As a user, I answer questions via text or voice and receive live transcript with confidence metrics. **Behaviors:** Real-time transcript, timer per question, AI evaluates answer quality (1–5 stars + written feedback).     | TBD          |
| **AI Mock Interviewer**         | Coaching & History       | As a user, I see improvement tips after each session and track progress over time. **Behaviors:** Saved transcripts, confidence trends chart, personalized coaching (e.g., "Be more specific with metrics").                  | TBD          |
| **Career Coaching**             | Skill Gap Analysis       | As a user, I chat with an AI coach to identify skill gaps based on my target roles. **Behaviors:** Chat interface, AI recommends courses/projects, links to free resources (freeCodeCamp, Udemy, etc.).                       | TBD          |
| **Job-Opening Alert Engine**    | Alert Setup              | As a user, I choose keywords, sources (LinkedIn, AngelList, Wellfound, RSS), and frequency (daily, weekly) for job alerts. **Behaviors:** Multi-select sources, keyword tags, preview alert volume estimate.                  | TBD          |
| **Job-Opening Alert Engine**    | Alert Delivery           | As a user, I receive job alerts via email and in-app notifications with "Apply-with-Profile" shortcut. **Behaviors:** Email digest format, in-app badge counter, one-click cover letter generation for each alert.            | TBD          |
| **Authentication**              | Signup                   | As a user, I can create an account with email + password to save my portfolio and enable job alerts. **Behaviors:** Email validation, password strength indicator, Supabase Auth integration, redirect to dashboard on success. | TBD          |
| **Authentication**              | Login                    | As a returning user, I can log in with email + password. **Behaviors:** "Remember me" checkbox, "Forgot password" link, redirect to dashboard with saved data.                                                               | TBD          |
| **Authentication**              | Forgot Password          | As a user, I can reset my password via email link. **Behaviors:** Email sent with magic link, link expires in 1 hour, success message on password update.                                                                    | TBD          |
| **Dashboard**                   | Overview                 | As a user, I see all generated assets (portfolio link, résumé download, optimizer score) and action buttons (cover letter, mock interview, job alerts). **Behaviors:** Persistent across sessions, edit/regenerate options.  | TBD          |

---

## 📐 Model Requirements

| SPECIFICATION          | REQUIREMENT                                   | RATIONALE                                                                                                                                     |
| ---------------------- | --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Open vs Proprietary    | **Open-source via Groq** (Llama 3.1 8B/70B, Mixtral) | Free API tier, fast inference, sufficient quality for structured tasks (résumé parsing, portfolio generation, mock interviews).               |
| Model Selection        | **User-configurable** (8B vs 70B toggle in settings) | Allows A/B testing speed vs. quality; 8B for fast tasks (parsing, optimizer), 70B for nuanced tasks (coaching, behavioral interview feedback). |
| Context Window         | **8K–32K tokens** (depending on model)        | Sufficient to process full résumé (2–4 pages = ~2K tokens) + job description (~500 tokens) + system prompts.                                 |
| Modalities             | **Text-only** (v1)                            | Voice input for mock interviews is future enhancement (post-hackathon); text input is faster to implement.                                   |
| Fine-Tuning Capability | **Not required for v1**                       | Few-shot prompting sufficient for structured outputs (JSON résumé schema, portfolio HTML template). Fine-tuning deferred to post-launch.     |
| Latency                | **P50: <2 sec, P95: <5 sec** (per API call)  | Groq's inference speed enables fast portfolio generation (<30 sec total including multiple API calls); critical for demo "wow" factor.        |
| Parameters             | **8B for speed, 70B for quality**             | 8B handles résumé parsing, keyword extraction, cover letter generation. 70B handles mock interview feedback and career coaching nuance.       |

---

## 🧮 Data Requirements

### Initial Data Collection
- **User-uploaded résumés:** PDF/Word files parsed via PyPDF2 or pdfplumber (Python libraries)
- **LinkedIn scraping:** If user provides URL, use BeautifulSoup or Playwright (fallback to manual input if blocked)
- **Guided Q&A responses:** Structured prompts collect work history, skills, education, projects, metrics

### Data Storage (Supabase)
**Tables:**
1. **users** (id, email, password_hash, created_at, subdomain)
2. **profiles** (user_id, work_history_json, skills_json, education_json, projects_json, contact_info_json, linkedin_url, original_resume_text)
3. **portfolios** (user_id, subdomain, html_content, css_content, live_url, last_updated)
4. **resumes** (user_id, pdf_url, docx_url, ats_score, last_updated)
5. **job_alerts** (user_id, keywords_array, sources_array, frequency, last_sent)
6. **mock_interviews** (user_id, role_type, transcript_json, confidence_score, feedback_text, created_at)
7. **cover_letters** (user_id, job_description_text, generated_letter_text, tone_preset, created_at)

### Data Preparation
- **Résumé parsing:** Extract structured fields (name, email, phone, work history with dates/titles/companies, skills, education, projects)
- **Validation:** Check for missing critical fields (name, contact info), prompt user to fill gaps
- **Normalization:** Standardize date formats, skill names (e.g., "React.js" vs "ReactJS"), job titles

### Ongoing Collection
- **Job alert scraping:** Daily cron job (Supabase Edge Functions or external service) queries LinkedIn/AngelList/Wellfound APIs or RSS feeds
- **Mock interview feedback:** Store transcripts + AI feedback for progress tracking
- **Optimizer history:** Track score improvements over time (user engagement metric)

### Iterative Improvement (Post-Hackathon)
- **Fine-tuning dataset:** Collect user edits to AI-generated cover letters and résumés to train custom model
- **Feedback loop:** Prompt users to rate AI outputs (1–5 stars) to build golden dataset for evaluation

---

## 💬 Prompt Requirements

### System Prompts (per feature)

**Résumé Parsing:**
```
You are a résumé parser. Extract structured data from the following résumé text and return JSON with fields: name, email, phone, linkedin_url, work_history (array of {title, company, dates, bullets}), skills (array), education (array of {degree, institution, year}), projects (array of {name, description, technologies}). If a field is missing, return null. Do not invent information.
```

**Portfolio Generation:**
```
You are a portfolio website generator. Given structured career data (work history, skills, projects, education), generate a complete responsive HTML page with inline CSS. Use a modern, professional design (flexbox layout, clean typography, subtle animations). Include sections: Hero (name + tagline), About, Work Experience, Projects (with links), Skills, Contact. Output only valid HTML with no markdown formatting.
```

**Cover Letter Generation:**
```
You are a cover letter writer. Given a job description and user career data (work history, skills, projects), write a tailored cover letter in [tone: formal/friendly/technical]. Structure: Intro (enthusiasm + company mention), Body (2–3 paragraphs matching user skills to job requirements with specific examples), Closing (call to action). Max 350 words. Do not use placeholder text like "[Your Name]"—use actual user data.
```

**Optimizer & Keyword Analysis:**
```
You are an ATS optimizer. Given a résumé and job description, score the résumé (0–100) based on keyword match, relevant experience, and formatting clarity. Identify missing keywords from the job description and suggest specific additions to the résumé. Output JSON: {score: int, missing_keywords: array, suggestions: array of {section: string, recommendation: string}}.
```

**Mock Interview (Question Generation):**
```
You are a technical interviewer for [role: Frontend/Backend/Fullstack/PM]. Generate 6 interview questions: 3 technical (specific to role, e.g., "Explain React hooks" for Frontend) and 3 behavioral (e.g., "Tell me about a time you debugged a production issue"). Output JSON array of {type: "technical"/"behavioral", question: string}.
```

**Mock Interview (Feedback):**
```
You are an interview coach. Given a user's answer to the question "[question]", evaluate it on: clarity (1–5), specificity (1–5), and relevance (1–5). Provide a confidence score (average of 3 metrics) and 2–3 bullet points of improvement tips. If the answer is too vague, suggest adding metrics or concrete examples. Output JSON: {confidence_score: float, clarity: int, specificity: int, relevance: int, feedback: array of strings}.
```

**Career Coaching:**
```
You are a career coach for early-career software engineers. Given user career data and target role, identify skill gaps (e.g., "You have React experience but the role requires TypeScript"). Recommend 2–3 free learning resources (courses, tutorials, projects) to close each gap. Be specific (e.g., "Complete freeCodeCamp's TypeScript course") and encouraging.
```

### Policy & Refusal Handling
- **Harmful content:** If user inputs offensive language or requests unethical advice (e.g., "lie on résumé"), respond: "I can't help with that. Let's focus on highlighting your real strengths."
- **Out-of-scope requests:** If user asks non-career questions (e.g., "What's the weather?"), respond: "I'm here to help with your career and job search. How can I assist with your portfolio, résumé, or interviews?"

### Personalization
- **Tone presets:** Cover letters support formal (corporate), friendly (startup), technical (engineer-to-engineer) tones—pass tone as parameter to prompt
- **Pronouns:** Extract from user profile or ask during signup; use in generated content (e.g., "they/them" in cover letters)

### Output Format Guarantees
- **JSON outputs:** All API responses for parsing, optimizer, and interview feedback use strict JSON schema (validated with Pydantic in Python)
- **HTML outputs:** Portfolio generation returns valid, lintable HTML (no unclosed tags, inline CSS only)

### Accuracy Target
- **Résumé parsing:** 95% field extraction accuracy on well-formatted résumés (validated in testing plan)
- **Cover letter relevance:** 80%+ user satisfaction (post-generation survey: "Would you use this letter?")

---

## 🧪 Testing & Measurement

### Pre-Launch (Hackathon Build)

**Unit Tests (if time permits):**
- Résumé parsing: Test 5 sample résumés (PDF + Word) with varying formats (chronological, functional, hybrid)
- Portfolio generation: Validate HTML output (no broken tags, responsive CSS)
- Supabase integration: Test CRUD operations (create user, save profile, retrieve portfolio)

**Manual Testing (Priority):**
- **Happy path:** Upload résumé → generate portfolio + résumé → download → verify subdomain works
- **Edge cases:** Upload malformed PDF → fallback to Q&A, paste invalid LinkedIn URL → show error, hit Groq rate limit → graceful error message
- **Cross-browser:** Test in Chrome, Firefox, Safari (Streamlit compatibility)
- **Mobile responsiveness:** Verify portfolio renders correctly on phone (use Chrome DevTools)

**Demo Rehearsal:**
- Run full flow 3+ times before hackathon demo to catch bugs
- Prepare fallback: Pre-generated portfolio if live generation fails during demo

### Post-Launch (Weeks 1–12)

**Offline Evaluation:**
- **Golden set:** Create 20 résumé samples (10 well-formatted, 10 edge cases) with expected outputs (JSON schema)
- **Pass threshold:** 95% field extraction accuracy, 0 crashes on valid inputs
- **Cover letter quality:** Human reviewers rate 50 generated letters (1–5 scale), target avg 4.0+

**Online Measurement (A/B Testing):**
- **Experiment 1:** Llama 8B vs 70B for cover letter generation → measure user edits (fewer edits = better quality)
- **Experiment 2:** Optimizer auto-rewrite vs manual suggestions → measure activation (% who regenerate résumé)
- **Guardrails:** If P95 latency >10 sec, auto-switch to faster model; if crash rate >5%, rollback and debug

**Live Performance Tracking:**
- **Dashboards (Streamlit + Supabase):**
  - Signups per day (line chart)
  - Activation funnel: Signups → Portfolio generated → Résumé downloaded → Cover letter created
  - Feature usage: % users who try mock interview, job alerts, optimizer
  - Latency: P50/P95 for portfolio generation, cover letter generation
  - Error rate: Failed API calls, parsing errors, Supabase timeouts

**Alerting:**
- **Critical:** If error rate >10% or P95 latency >30 sec, send email alert (Supabase webhooks + Sendgrid)
- **Rollback plan:** If Groq API is down, show maintenance message and queue requests for retry

---

## ⚠️ Risks & Mitigations

| RISK                                              | MITIGATION                                                                                                                                           |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **24-hour timeline too aggressive for 7 features** | Pre-build résumé parsing + portfolio template before hackathon; use Streamlit's rapid prototyping; prioritize demo flow over polish.                |
| **Groq API rate limit hit during demo**           | Cache sample outputs for demo; implement retry logic with exponential backoff; have pre-generated examples as fallback.                             |
| **Résumé parsing fails on unusual formats**       | Fallback to guided Q&A if parsing confidence <70%; show user "We couldn't parse your résumé—let's build one from scratch" message.                  |
| **Portfolio generation takes >30 sec (feels slow)** | Use Llama 8B for speed; show engaging progress messages ("Analyzing your skills...", "Building your site..."); optimize prompt length.               |
| **Job alert scraping blocked by LinkedIn/sites**  | Use official APIs where available (LinkedIn API requires approval—defer to post-hackathon); fallback to RSS feeds or manual job board aggregation.  |
| **Mock interview transcript quality is poor**     | Use Llama 70B for interview feedback; implement confidence thresholds (if <50%, prompt user to elaborate); save transcripts for manual review.      |
| **User data privacy concerns (résumés, PII)**     | Store résumés encrypted at rest (Supabase storage encryption); allow user deletion of all data ("Delete my account" button); no third-party sharing. |
| **Streamlit hosting limits (free tier)**          | Deploy on Streamlit Cloud free tier (3 apps, sufficient for demo); post-hackathon migrate to Vercel or Railway if scaling needed.                   |
| **Supabase free tier exhausted (storage/queries)** | Monitor usage daily; optimize queries (avoid N+1, use indexes); upgrade to Pro tier ($25/mo) if user count exceeds 1,000.                           |
| **Invalid JSON breaks optimizer/interview flows** | Wrap all Groq API calls in try-except; validate JSON with Pydantic; auto-retry with repaired prompt; show graceful error ("Try again" button).      |

---

## 💰 Costs

### Development Costs (24-hour hackathon)
- **Time investment:** 24 hours solo dev (opportunity cost)
- **Pre-existing skills/tools:** Python, Streamlit, Groq API, Supabase (assumed—no learning curve)
- **Data costs:** $0 (using free APIs and sample résumés for testing)

### Operational Costs (Post-Hackathon, Weeks 1–12)

**Free Tier (Target for first 500 users):**
- **Groq API:** Free tier includes 14,400 requests/day (Llama 8B), 7,200/day (70B)—sufficient for 500 users generating ~3 assets each per day
- **Supabase:** Free tier includes 500MB storage, 2GB bandwidth, 50MB database—sufficient for 500 user profiles + résumés
- **Streamlit Cloud:** Free tier includes 1 app, unlimited viewers—sufficient for demo and early users
- **Domain:** $12/year for custom domain (portfolioai.app)—optional, use Streamlit default URL for hackathon

**Paid Tier (If scaling beyond 500 users):**
- **Groq API:** $0.10–0.50 per 1M tokens (estimate $50/month for 2,000 users)
- **Supabase Pro:** $25/month (8GB storage, 50GB bandwidth)
- **Vercel/Railway hosting:** $20/month (faster than Streamlit Cloud, custom domain support)
- **SendGrid email:** Free tier 100 emails/day (job alerts), $15/month for 40,000 emails (sufficient for 1,000 users with daily alerts)

**Total estimated cost (Months 1–3, 500 users):** $12/year domain = **~$1/month**
**Total estimated cost (Months 1–3, 2,000 users):** Domain + Groq + Supabase + hosting + email = **~$110/month**

---

## 🔗 Assumptions & Dependencies

### Assumptions
1. **Groq API free tier is sufficient for hackathon demo and first 500 users** (14K+ requests/day covers 500 users × 3 assets/day)
2. **Résumé parsing accuracy >90% on well-formatted PDFs** (chronological format, standard fonts, no heavy graphics)
3. **LinkedIn scraping is not critical for v1** (fallback to upload or Q&A if blocked—no legal risk)
4. **Users are comfortable with temporary session persistence** (local storage) if they skip signup initially
5. **Streamlit + shadcn UI integration is feasible** (assume shadcn components can be embedded via custom HTML/CSS)
6. **Job alert scraping can use RSS feeds or basic web scraping** (no official APIs required for v1—AngelList/Wellfound have public RSS)
7. **Mock interview text-based input is sufficient for v1** (voice input deferred to post-hackathon)
8. **Portfolio hosting on custom subdomains is achievable via Streamlit or static HTML export** (user gets link like user123.portfolioai.app)
9. **No fine-tuning required for v1** (few-shot prompting sufficient for quality outputs)
10. **User feedback collection (surveys, ratings) can be added post-hackathon** (not required for demo)

### Dependencies
1. **Groq API uptime** (if Groq is down during demo, fallback to cached examples)
2. **Supabase uptime** (user data persistence requires Supabase; fallback to in-memory storage if down)
3. **PyPDF2 or pdfplumber library** (résumé parsing depends on these Python libraries)
4. **Streamlit framework** (entire UI built on Streamlit—no alternative planned)
5. **shadcn component library** (UI polish depends on integrating shadcn styles)
6. **Custom subdomain routing** (depends on DNS setup or dynamic routing—may require post-hackathon infra work)
7. **Email delivery service** (job alerts require SendGrid or similar—fallback to in-app notifications only)
8. **Browser compatibility** (Streamlit apps require modern browsers—IE not supported)
9. **Internet connectivity during demo** (live API calls require stable connection—have offline fallback)
10. **User willingness to upload résumés or provide career data** (product fails if users are unwilling to share PII)

---

## 🔒 Compliance/Privacy/Legal

### Data Privacy
- **PII handling:** Résumés contain names, emails, phone numbers, addresses—classified as PII
- **Storage:** All user data stored in Supabase with encryption at rest (Supabase default)
- **Retention:** Users can delete their account and all associated data at any time ("Delete Account" button in settings)
- **Third-party sharing:** Zero third-party data sharing (Groq API does not store user prompts per their policy—verify before launch)
- **Cookies/tracking:** Minimal cookies (Supabase Auth session tokens only); no Google Analytics or third-party trackers for v1

### Regulatory Compliance
- **GDPR (if EU users):** Provide "Export my data" (download JSON of all user data) and "Delete my data" features; include privacy policy link in footer
- **CCPA (if California users):** Same as GDPR (data export + deletion)
- **Terms of Service:** Draft simple ToS covering: (1) user owns their data, (2) AI-generated content may contain errors, (3) no guarantees of job success
- **Privacy Policy:** Draft covering: (1) what data is collected (résumés, contact info), (2) how it's used (portfolio generation, job alerts), (3) no selling/sharing, (4) user deletion rights

### Legal Risks
- **LinkedIn scraping:** Violates LinkedIn ToS (hiQ Labs case precedent is murky)—**mitigation:** make LinkedIn input optional, prioritize upload/Q&A, defer scraping to post-hackathon with legal review
- **Job board scraping:** Some job boards prohibit scraping—**mitigation:** use official APIs where available (AngelList, Wellfound), respect robots.txt, add user-agent headers
- **AI-generated content liability:** Users may submit AI-generated cover letters with errors—**mitigation:** add disclaimer "Review AI-generated content before submitting to employers"
- **Copyright (portfolio templates):** Ensure generated HTML does not infringe on purchased themes—**mitigation:** build custom template from scratch or use MIT-licensed open-source templates

### Accessibility
- **WCAG 2.1 AA compliance:** Ensure portfolio sites have sufficient color contrast, alt text for images, keyboard navigation—**v1 scope:** partial compliance (focus on contrast + semantic HTML), full audit post-hackathon
- **Screen reader support:** Streamlit has limited screen reader support—**mitigation:** add ARIA labels where possible, note as "in progress" for v1

---

## 📣 GTM/Rollout Plan

### Pre-Launch (Hackathon Week)
**Milestone 1: Core Build (Hours 0–16)**
- Hours 0–4: Setup (Streamlit app scaffold, Supabase schema, Groq API integration, auth flow)
- Hours 4–8: Résumé parsing + portfolio generation (highest priority)
- Hours 8–12: CV generator (Q&A flow) + cover letter writer
- Hours 12–16: Optimizer + mock interviewer (basic versions)

**Milestone 2: Polish & Integration (Hours 16–22)**
- Hours 16–18: Job alert setup UI (backend scraping deferred to post-demo)
- Hours 18–20: Career coaching chat interface (basic Q&A)
- Hours 20–22: Dashboard integration, bug fixes, UI polish (shadcn styling)

**Milestone 3: Demo Prep (Hours 22–24)**
- Hours 22–23: End-to-end testing, demo script rehearsal
- Hours 23–24: Deploy to Streamlit Cloud, test live URL, prepare fallback examples

### Launch Strategy
**Hackathon Demo (Hour 24):**
- **Demo script (2 minutes):**
  1. Show landing page → upload sample résumé (pre-prepared)
  2. Live generation → portfolio site appears in 20 seconds
  3. Download résumé, show optimizer score
  4. Generate cover letter (paste job description)
  5. Start mock interview (answer 1 question, show feedback)
  6. Highlight job alerts + career coaching (screenshots if not live)
- **Ask:** "Who here has spent hours building a portfolio? PortfolioAI does it in minutes."

**Post-Hackathon Soft Launch (Weeks 1–4):**
- Share on Twitter/LinkedIn with demo video
- Post to Hacker News "Show HN: PortfolioAI—AI portfolio + résumé generator for bootcamp grads"
- Post to Product Hunt (prepare 3 screenshots, tagline, first comment)
- Share in bootcamp communities (Reddit: r/learnprogramming, r/cscareerquestions; Discord: 100Devs, freeCodeCamp)
- Collect feedback via Typeform survey (embedded in app): "How likely are you to recommend PortfolioAI? What features do you want next?"

### Phased Rollout
**Phase 1 (Weeks 1–4): Beta (Invite-Only)**
- Target 100 users from personal network + bootcamp communities
- Focus: Validate core activation (portfolio + résumé generation)
- Collect qualitative feedback (user interviews, surveys)
- Fix critical bugs (parsing errors, slow generation, broken subdomains)

**Phase 2 (Weeks 5–8): Public Launch**
- Remove invite gate, open to all signups
- Launch job alerts (implement scraping or API integrations)
- Add social sharing ("Share your portfolio on LinkedIn")
- Target 500 signups via Hacker News, Product Hunt, bootcamp partnerships

**Phase 3 (Weeks 9–12): Growth & Iteration**
- Add premium features (custom domain for portfolio, premium résumé templates, unlimited mock interviews)
- Implement referral program ("Invite 3 friends, get premium free for 1 month")
- Partner with bootcamps (offer white-label version or affiliate program)
- Optimize for retention (email drip campaign: "You haven't practiced interviews in 7 days—let's fix that")

**Success Metrics by Phase:**
- Phase 1: 100 signups, 70% activation, 20+ feedback responses
- Phase 2: 500 signups, 70% activation, 50% D7 retention
- Phase 3: 1,500 signups, 75% activation, 55% D7 retention, 10% conversion to premium (if added)

---

**END OF PRD**

---

**Next Steps:**
1. Review this PRD and flag any sections that need revision (scope, risks, KPIs)
2. Confirm assumptions (especially LinkedIn scraping deferral, Groq API quota)
3. Begin Hour 0 setup: Streamlit scaffold + Supabase schema + Groq test API call

Questions? Let's refine before you start building! 🚀
