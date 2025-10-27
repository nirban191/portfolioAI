# 🚀 Quick Start Guide - Test in 5 Minutes

## Step 1: Install Dependencies (2 min)

```bash
cd /Users/nirbanbiswas/Desktop/100x/code/hackathon

# Install all Python packages
pip install -r requirements.txt
```

## Step 2: Set Up Supabase Database (2 min)

1. Go to your Supabase project: [https://supabase.com/dashboard/project/ngplmgtrlkhgkkgibymq](https://supabase.com/dashboard/project/ngplmgtrlkhgkkgibymq)

2. Click "SQL Editor" in the left sidebar

3. Click "New Query"

4. Copy the ENTIRE contents of `schema.sql` and paste into the editor

5. Click "Run" (or press Cmd/Ctrl + Enter)

6. Wait for "Success" message

7. **Create Storage Buckets:**
   - Click "Storage" in left sidebar
   - Click "New bucket"
   - Name: `resumes`, Make it **Private**, Click "Create"
   - Click "New bucket" again
   - Name: `portfolios`, Make it **Public**, Click "Create"

## Step 3: Run the App (1 min)

```bash
streamlit run app.py
```

Your browser will open at `http://localhost:8501` automatically.

## Step 4: Test Core Features

### Test Resume Upload

1. You'll see the landing page with 3 input options
2. Click the file uploader in the first column
3. **Need a test resume?** Use one of these:
   - Your own resume PDF
   - Or create a simple test resume with any text editor

4. Click "🎨 Generate Portfolio"
5. Watch the progress bar (takes 20-40 seconds):
   - Parsing resume...
   - Generating portfolio...
   - Creating resume files...

6. You'll be redirected to the dashboard
7. **Download your files:**
   - Click "⬇️ Download Portfolio HTML"
   - Click "⬇️ Download PDF"
   - Click "⬇️ Download DOCX"

8. Open the portfolio.html file in your browser to see your generated site!

### Test LinkedIn Import (Optional)

1. Click "🔙 Start Over"
2. Paste a LinkedIn URL: `linkedin.com/in/yourname`
3. Click "🎨 Generate Portfolio"

**Note**: LinkedIn often blocks automated requests. If it fails, that's expected - just use resume upload instead.

## 🎉 Success Indicators

✅ **Working correctly if you see:**
- Progress bar completes without errors
- Dashboard shows your name
- Portfolio HTML downloads successfully
- Resume PDF and DOCX download successfully
- Quick stats show your work experience, skills, projects counts

❌ **Common issues:**

**"Failed to initialize services"**
- Check that `.env` file exists in the project root
- Verify Supabase credentials are correct

**"Could not extract text from PDF"**
- Try a different resume format
- Make sure PDF is text-based (not scanned image)

**"Rate limit exceeded"**
- Wait a few minutes (Groq free tier has limits)
- Or upgrade to Groq paid tier

## 📊 What Just Happened?

1. **AI parsed your resume** using Groq's Llama 3.1 8B model
2. **Extracted structured data** (name, skills, work history, projects, education)
3. **Generated a portfolio website** with AI (responsive HTML/CSS)
4. **Created ATS-optimized resumes** in PDF and DOCX formats
5. **Stored everything** in Supabase (if you had created an account)

## 🚀 Next: Try Additional Features

Go to the dashboard tabs:

**✉️ Cover Letter Tab**
- Paste a job description
- Select tone (formal/friendly/technical)
- Click "Generate" (coming in next iteration)

**🎯 Optimizer Tab**
- Paste a target job description
- See mock ATS score and missing keywords
- Click "Analyze" (coming in next iteration)

**🚀 More Features Sidebar**
- Mock Interview (UI mockup)
- Job Alerts (UI mockup)
- Career Coach (UI mockup)

## 🐛 Troubleshooting

### Check Logs

If something fails, check the terminal where you ran `streamlit run app.py` for error messages.

### Test Supabase Connection

```python
python
>>> from utils.supabase_client import get_supabase_client
>>> client = get_supabase_client()
>>> print("✅ Supabase connected!")
```

### Test Groq API

```python
python
>>> from utils.groq_client import get_groq_client
>>> client = get_groq_client()
>>> result = client.call_api("You are helpful", "Say hello", model="8b")
>>> print(result)
```

### Check File Permissions

```bash
ls -la utils/
ls -la assets/
ls -la prompts/
```

All Python files should have read permissions.

## 📝 Sample Test Resume Text

If you don't have a resume handy, create a file called `test_resume.txt` with:

```
John Doe
john.doe@email.com | 555-123-4567 | linkedin.com/in/johndoe

WORK EXPERIENCE

Software Engineer Intern | TechCorp Inc. | June 2023 - Dec 2023
- Built React components for dashboard, improving load time by 40%
- Implemented RESTful APIs using Node.js and Express
- Collaborated with design team on UI/UX improvements

SKILLS
JavaScript, React, Node.js, Python, SQL, Git, AWS

EDUCATION
Bachelor of Science in Computer Science | State University | 2024

PROJECTS

Weather Dashboard
- Real-time weather app using OpenWeather API
- Technologies: React, Node.js, Express, MongoDB
- GitHub: github.com/johndoe/weather-app
```

Save as PDF and upload!

## ✅ Success Checklist

- [ ] Dependencies installed without errors
- [ ] Supabase schema ran successfully
- [ ] Storage buckets created (resumes + portfolios)
- [ ] App starts at localhost:8501
- [ ] Can upload resume and see parsing progress
- [ ] Dashboard shows after generation
- [ ] Portfolio HTML downloads
- [ ] Resume PDF downloads
- [ ] Resume DOCX downloads

## 🎯 Ready for Hackathon Demo!

Once all checklist items pass, you're ready to:
1. Prepare your demo script (2 minutes)
2. Have 2-3 sample resumes ready
3. Test the full flow one more time
4. Deploy to Hugging Face Spaces (see README.md)

**Demo Flow:**
1. Show landing page (10 sec)
2. Upload resume (5 sec)
3. Show AI generation progress (20 sec)
4. Show dashboard with downloads (15 sec)
5. Open portfolio HTML in browser (10 sec)
6. Quick tour of additional features (30 sec)

Total: 90 seconds + Q&A

---

**Need help?** Check the full [README.md](README.md) or terminal output for error messages.
