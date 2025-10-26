# 🎨 PortfolioAI

> AI-Powered Career Toolkit - Transform your resume into a stunning portfolio, optimize for ATS, and ace your interviews

[![Deploy on Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/nirban191/PortfolioAI)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

### 🎯 Core Features
- **📄 Smart Resume Parser** - Upload PDF/DOCX resumes or scrape LinkedIn profiles
- **🌐 AI Portfolio Generator** - Generate beautiful, responsive portfolio websites (Stripe-inspired design)
- **📝 Resume Builder** - Export optimized resumes in PDF/DOCX formats
- **✍️ Cover Letter Generator** - Create tailored cover letters in multiple tones (Formal, Friendly, Technical)

### 🚀 Advanced Tools
- **🎯 ATS Optimizer** - Analyze and optimize your resume for Applicant Tracking Systems
- **🎤 Mock Interview Prep** - Practice with AI-generated interview questions and get feedback
- **💬 AI Career Coach** - Get personalized career advice and guidance
- **🔐 User Authentication** - Secure Supabase-powered auth and data storage

## 🎨 Design Philosophy

PortfolioAI generates portfolios with a **Stripe-inspired design aesthetic**:
- Clean, professional, and minimal
- Stripe Purple (#635BFF), Navy (#0A2540), and Slate (#425466) color palette
- Soft shadows for depth
- Generous whitespace
- Trustworthy, corporate-friendly appearance

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python 3.9+
- **AI/LLM**: Groq (Llama 3.3 70B, Llama 3.1 8B, Mixtral 8x7B)
- **Database**: Supabase (PostgreSQL + Auth)
- **PDF Processing**: PyPDF2, pdfplumber, ReportLab
- **Document Generation**: python-docx
- **Web Scraping**: BeautifulSoup, Playwright

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/PortfolioAI.git
cd PortfolioAI
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
GROQ_API_KEY=your_groq_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

4. **Run the application**
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## 🔑 Getting API Keys

### Groq API Key
1. Visit [console.groq.com](https://console.groq.com/keys)
2. Sign up or log in
3. Create a new API key
4. Copy and paste into your `.env` file

### Supabase Credentials
1. Visit [supabase.com](https://supabase.com/dashboard)
2. Create a new project
3. Go to Settings → API
4. Copy the Project URL and anon/public key
5. Paste into your `.env` file

## 🚀 Deployment

### Deploy to Hugging Face Spaces

1. **Fork/Clone this repository**

2. **Create a new Space** on [Hugging Face](https://huggingface.co/new-space)
   - Choose "Docker" as the SDK
   - Link your GitHub repository

3. **Add secrets** in Space Settings → Repository secrets:
   - `GROQ_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`

4. **Deploy!** - Your Space will automatically build and deploy

## 📁 Project Structure

```
PortfolioAI/
├── app.py                      # Main Streamlit application
├── assets/
│   └── style.css              # Custom CSS styling
├── prompts/
│   └── prompts.py             # AI system prompts
├── utils/
│   ├── groq_client.py         # Groq AI client wrapper
│   ├── supabase_client.py     # Supabase client wrapper
│   ├── resume_parser.py       # PDF/DOCX resume parser
│   ├── linkedin_scraper.py    # LinkedIn profile scraper
│   ├── portfolio_generator.py # Portfolio HTML generator
│   ├── resume_generator.py    # Resume PDF/DOCX generator
│   └── validators.py          # Input validation
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration for HF Spaces
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🎯 Usage

### 1. Upload Resume or LinkedIn Profile
- **Option A**: Upload your existing resume (PDF/DOCX)
- **Option B**: Paste your LinkedIn profile URL
- **Option C**: Fill out the guided Q&A form

### 2. Generate Portfolio
- AI analyzes your data and generates a professional portfolio
- Choose from multiple AI models (8B fast, 70B best quality, Mixtral balanced)
- Download as HTML file or deploy online

### 3. Create Documents
- **Resume**: Export in PDF or DOCX format
- **Cover Letter**: Generate tailored letters for job applications

### 4. Optimize & Prepare
- **ATS Optimizer**: Get a score and improvement suggestions
- **Mock Interview**: Practice with AI-generated questions
- **Career Coach**: Get personalized career advice

## 🤖 AI Models

PortfolioAI supports multiple LLM models via Groq:

| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| Llama 3.1 8B | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | Quick tasks, iterations |
| Llama 3.3 70B | ⚡ Slow | ⭐⭐⭐⭐⭐ Excellent | Best quality, final output |
| Mixtral 8x7B | ⚡⚡ Medium | ⭐⭐⭐⭐ Very Good | Balanced performance |

## 🔒 Privacy & Security

- **Local Processing**: All data processing happens on your device or in your Supabase instance
- **Secure Auth**: Supabase handles authentication securely
- **No Data Retention**: AI providers (Groq) don't retain your data
- **Environment Variables**: Sensitive keys stored in `.env` (never committed)

## 🐛 Troubleshooting

### Common Issues

**"Failed to initialize services"**
- Make sure `.env` file exists with correct credentials
- For HF Spaces: Add secrets in Settings → Repository secrets

**Scroll stuttering/lag**
- The app uses optimized CSS for smooth scrolling
- Try disabling browser extensions
- Use a modern browser (Chrome, Firefox, Safari, Edge)

**Resume parsing errors**
- Ensure PDF/DOCX is not password-protected
- Try a different file format
- Check that the file is a valid resume document

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Powered by [Groq](https://groq.com) AI
- Backend by [Supabase](https://supabase.com)
- Design inspired by [Stripe](https://stripe.com)

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ for the 100x Hackathon**
