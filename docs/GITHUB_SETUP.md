# 🚀 GitHub Repository Setup Instructions

## Step 1: Create GitHub Repository

1. **Go to GitHub**: Visit https://github.com/new

2. **Repository Settings**:
   - **Repository name**: `PortfolioAI`
   - **Description**: `🎨 AI-Powered Career Toolkit - Transform your resume into a stunning portfolio`
   - **Visibility**: Public (or Private if you prefer)
   - **❌ DO NOT** initialize with README, .gitignore, or license (we already have these)

3. **Click**: "Create repository"

## Step 2: Connect Your Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add GitHub as a remote (replace YOUR_USERNAME with your GitHub username)
git remote add github https://github.com/YOUR_USERNAME/PortfolioAI.git

# Or if using SSH:
git remote add github git@github.com:YOUR_USERNAME/PortfolioAI.git

# Push your code to GitHub
git push github main
```

## Step 3: Keep Both Remotes (GitHub + Hugging Face)

You can keep both remotes and push to both:

```bash
# View all remotes
git remote -v

# You should see:
# origin  https://huggingface.co/spaces/nirban191/PortfolioAI (HF Spaces)
# github  https://github.com/YOUR_USERNAME/PortfolioAI.git (GitHub)

# Push to both:
git push origin main   # Pushes to Hugging Face Spaces
git push github main   # Pushes to GitHub
```

## Step 4: Update README Badge

After creating the repo, update line 53 in README.md:

```markdown
# Change this:
git clone https://github.com/YOUR_USERNAME/PortfolioAI.git

# To your actual GitHub URL:
git clone https://github.com/nirban191/PortfolioAI.git
```

## Quick Commands Summary

```bash
# 1. Add GitHub remote
git remote add github https://github.com/YOUR_USERNAME/PortfolioAI.git

# 2. Push to GitHub
git push github main

# 3. Set up branch tracking (optional)
git branch --set-upstream-to=github/main main

# 4. Future pushes to both
git push origin main && git push github main
```

## Alternative: Use GitHub CLI (if you install it later)

```bash
# Install GitHub CLI (macOS)
brew install gh

# Authenticate
gh auth login

# Create repo and push in one command
gh repo create PortfolioAI --public --source=. --remote=github --push
```

## Verification

After pushing, verify your repo is live:
- Visit: `https://github.com/YOUR_USERNAME/PortfolioAI`
- You should see all your files, README, and LICENSE

## Notes

- ✅ Your .env file is already in .gitignore (won't be pushed)
- ✅ LICENSE is MIT (allows others to use your code)
- ✅ README has all documentation
- ✅ Code is ready to share with the world!

---

**Need help?** Check the status with `git status` or `git remote -v`
