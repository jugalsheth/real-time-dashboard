# ⚡ Quick Deploy Guide

## 🛑 Stop Local Server (Already Done!)
✅ Streamlit processes have been stopped

## 📦 Prepare for GitHub

```bash
cd real-time-dashboard

# Verify security (secrets.toml should be ignored)
git check-ignore .streamlit/secrets.toml

# Add all files
git add .

# Commit
git commit -m "Initial commit: Real-time analytics dashboard with advanced features"
```

## 🐙 Create GitHub Repository

### Option 1: GitHub Website (Easiest)
1. Go to: https://github.com/new
2. Repository name: `real-time-dashboard`
3. Description: "Real-time analytics dashboard for data pipeline monitoring"
4. Choose **Public** (or Private)
5. **DO NOT** check "Add README" (we already have one)
6. Click "Create repository"

### Option 2: GitHub CLI
```bash
gh repo create real-time-dashboard --public --source=. --remote=origin --push
```

### Option 3: Manual Push
```bash
# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/real-time-dashboard.git

# Push
git branch -M main
git push -u origin main
```

## ☁️ Deploy to Streamlit Cloud

1. **Visit**: https://share.streamlit.io
2. **Sign in** with GitHub
3. **Click** "New app"
4. **Select**:
   - Repository: `real-time-dashboard`
   - Branch: `main`
   - Main file: `app.py`
5. **Click** "Deploy"
6. **Wait** 1-2 minutes
7. **Get URL**: `https://your-app-name.streamlit.app`

## 🔗 Update Portfolio

Edit `src/portfolio.js`:

```javascript
{
  projectName: "Real-Time Analytics Dashboard",
  projectDesc: "Live monitoring dashboard...",
  embedUrl: "https://your-app-name.streamlit.app", // ← Your URL
  footerLink: [
    { name: "Live Demo", url: "https://your-app-name.streamlit.app" },
    { name: "GitHub", url: "https://github.com/YOUR_USERNAME/real-time-dashboard" }
  ]
}
```

## ✅ Security Checklist

- [x] `.streamlit/secrets.toml` is in `.gitignore`
- [x] No hardcoded API keys in code
- [x] Only `secrets.toml.example` is committed
- [x] All sensitive files ignored

## 🎉 Done!

Your dashboard is now:
- ✅ Secure (no secrets committed)
- ✅ On GitHub
- ✅ Deployed to Streamlit Cloud
- ✅ Ready to embed in portfolio

---

**Need help?** See `DEPLOY_TO_STREAMLIT.md` for detailed instructions.

