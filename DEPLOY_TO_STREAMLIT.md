# 🚀 Deploy to Streamlit Cloud - Step by Step

## Prerequisites
- ✅ GitHub account
- ✅ Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

## Step 1: Initialize Git Repository

```bash
cd real-time-dashboard

# Initialize git (if not already done)
git init

# Check what will be committed (verify secrets.toml is NOT listed)
git status

# Add all files (secrets.toml should be ignored)
git add .

# Verify .gitignore is working
git check-ignore .streamlit/secrets.toml
# Should output: .streamlit/secrets.toml

# Create initial commit
git commit -m "Initial commit: Real-time analytics dashboard"
```

## Step 2: Create GitHub Repository

### Option A: Using GitHub CLI (if installed)
```bash
gh repo create real-time-dashboard --public --source=. --remote=origin --push
```

### Option B: Using GitHub Website
1. Go to [github.com/new](https://github.com/new)
2. Repository name: `real-time-dashboard`
3. Description: "Real-time analytics dashboard for data pipeline monitoring"
4. Choose **Public** (or Private if you prefer)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### Option C: Manual Push
```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/real-time-dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app" button
   - Select your GitHub account
   - Repository: `real-time-dashboard`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: (choose a custom name or use default)

3. **Configure Secrets (if needed)**
   - Click "Advanced settings"
   - Go to "Secrets" tab
   - Add any API keys if you're using real data sources:
   ```toml
   [api_keys]
   github_token = "your_token_here"
   ```
   - **Note**: For simulated data (current setup), no secrets needed!

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment (usually 1-2 minutes)
   - Your app will be live at: `https://your-app-name.streamlit.app`

## Step 4: Update Portfolio

Once deployed, update your portfolio:

1. **Get your Streamlit URL**
   - Format: `https://your-app-name.streamlit.app`

2. **Update portfolio.js**
   ```javascript
   {
     projectName: "Real-Time Analytics Dashboard",
     projectDesc: "Live monitoring dashboard...",
     embedUrl: "https://your-app-name.streamlit.app", // ← Your URL here
     footerLink: [
       { name: "Live Demo", url: "https://your-app-name.streamlit.app" },
       { name: "GitHub", url: "https://github.com/YOUR_USERNAME/real-time-dashboard" }
     ]
   }
   ```

## Step 5: Verify Security

Before pushing, verify no secrets are committed:

```bash
# Check for potential secrets in code
grep -r "password\|token\|key" --include="*.py" | grep -v "#" | grep -v "example"

# Verify secrets.toml is ignored
git check-ignore .streamlit/secrets.toml

# Check what's being committed
git status
```

## ✅ Deployment Checklist

- [ ] Git repository initialized
- [ ] `.gitignore` includes `secrets.toml`
- [ ] No secrets in committed files
- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud app created
- [ ] App deployed successfully
- [ ] Portfolio updated with new URL
- [ ] Tested embedded dashboard in portfolio

## 🔧 Troubleshooting

### Issue: "Module not found" error
**Solution**: Make sure `requirements.txt` includes all dependencies

### Issue: App won't load
**Solution**: Check Streamlit Cloud logs for errors

### Issue: Secrets not working
**Solution**: 
- Verify secrets are added in Streamlit Cloud settings
- Use `st.secrets.get()` to access them
- Check secret names match exactly

### Issue: Auto-refresh too fast
**Solution**: Adjust `update_interval` in sidebar (minimum 1 second)

## 📚 Next Steps

1. **Customize**: Add your branding/colors
2. **Connect Real Data**: See `DATA_SOURCE_EXPLANATION.md`
3. **Add Authentication**: For production use
4. **Monitor**: Check Streamlit Cloud analytics

---

**Your dashboard is now live and secure! 🎉**

