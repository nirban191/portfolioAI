---
title: PortfolioAI
emoji: 🎨
colorFrom: pink
colorTo: blue
sdk: streamlit
sdk_version: 1.32.0
app_file: app.py
pinned: false
license: mit
---

# PortfolioAI - Your AI-Powered Career Companion

Transform your career journey with AI-powered tools for portfolio generation, resume optimization, interview prep, and career coaching—all in under 2 minutes.

## 🚀 Features

### Core Tools
- **🎨 AI Portfolio Builder**: Upload resume → Get a stunning, responsive portfolio website
- **📄 ATS Resume Generator**: Export optimized PDF + DOCX resumes that pass ATS systems
- **✉️ Smart Cover Letters**: Generate tailored cover letters in 3 tones (formal, friendly, technical) with PDF/DOCX/TXT export
- **🎯 Resume Optimizer**: ATS score analysis with keyword matching and recommendations

### AI-Powered Career Tools
- **🎤 Mock Interview**: AI-generated interview questions tailored to your profile with instant feedback
- **💬 AI Career Coach**: Interactive chatbot for career advice, salary tips, skill gaps, and job search strategy
- **✨ Q&A Flow**: Build your portfolio from scratch without a resume

### Data Input Options
- Upload resume (PDF/DOCX)
- LinkedIn profile import
- Manual Q&A form

## 🤖 Powered by Advanced AI

Built with **Groq AI (Llama 3.3 70B)** for lightning-fast, intelligent responses. Choose from 3 AI models:
- ⚡ Llama 3.1 8B (Fast)
- 🧠 Llama 3.3 70B (Best Quality)
- 🔀 Mixtral 8x7B (Balanced)

## 🔐 Setup & Configuration

This app requires the following secrets to be configured in your Hugging Face Space settings:

### Required Secrets

1. **GROQ_API_KEY**: Get your free API key from [Groq Cloud](https://console.groq.com)
2. **SUPABASE_URL**: Your Supabase project URL
3. **SUPABASE_KEY**: Your Supabase anon/public API key

### Setting up Secrets

Go to your Space Settings → Repository secrets and add:

```
GROQ_API_KEY=your_groq_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here
```

## 📊 Tech Stack

- **Frontend**: Streamlit
- **AI/LLM**: Groq AI (Llama 3.3 70B, Mixtral 8x7B)
- **Database**: Supabase (PostgreSQL)
- **Auth**: Supabase Auth
- **PDF Generation**: ReportLab
- **DOCX Generation**: python-docx

## 🎯 How to Use

1. **Choose Input Method**: Upload resume, paste LinkedIn profile, or use Q&A form
2. **Generate Assets**: AI creates portfolio, resume, and more in < 2 minutes
3. **Download Everything**: Get HTML portfolio, PDF/DOCX resumes, cover letters
4. **Optimize & Practice**: Use AI tools for resume optimization and interview prep
5. **Get Career Guidance**: Chat with AI career coach for personalized advice

## 📝 Features in Detail

### Portfolio Generation
- Stunning Framer-inspired design with gradients
- Fully responsive HTML
- Instant download
- Subdomain preview

### Resume Optimization
- ATS scoring (0-100)
- Keyword gap analysis
- Section-specific recommendations
- Strengths identification

### Mock Interview
- Technical, Behavioral, System Design, or Mixed questions
- 3-10 questions per session
- AI feedback on your answers
- Key points and common mistakes highlighted

### Career Coach Chatbot
- Interactive conversation
- Context-aware responses
- 7 career topics + custom questions
- Chat history export

## 🔒 Privacy & Security

- Demo mode available (no signup required, data not saved)
- User authentication for data persistence
- Row-level security in Supabase
- Environment variables for sensitive data

## 📄 License

MIT License - feel free to fork and customize!

## 🙏 Acknowledgments

Built with Streamlit, Groq AI (Llama 3.3), and Supabase
