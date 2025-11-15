# ⚡ Quick Start Guide

## 1. Test Locally (2 minutes)

```bash
cd real-time-dashboard
pip install -r requirements.txt
streamlit run app.py
```

Open: http://localhost:8501

## 2. Deploy to Streamlit Cloud (5 minutes)

1. **Create GitHub repo** (if you haven't)
   ```bash
   git init
   git add .
   git commit -m "Real-time analytics dashboard"
   git remote add origin https://github.com/YOUR_USERNAME/real-time-dashboard.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select repo: `real-time-dashboard`
   - Main file: `app.py`
   - Click "Deploy"

3. **Get your URL**
   - Format: `https://your-app-name.streamlit.app`
   - Copy this URL!

## 3. Add to Portfolio (1 minute)

Edit `src/portfolio.js`:

```javascript
{
  projectName: "Real-Time Analytics Dashboard",
  projectDesc: "Live monitoring dashboard...",
  embedUrl: "https://your-app-name.streamlit.app", // ← Paste your URL here
  footerLink: [
    { name: "Live Demo", url: "https://your-app-name.streamlit.app" },
    { name: "GitHub", url: "https://github.com/jugalsheth/real-time-dashboard" }
  ]
}
```

## 4. Test in Portfolio

```bash
npm start
```

Visit your portfolio and check the Projects section!

## 🎉 Done!

Your dashboard is now live and embedded in your portfolio.

---

## Next: Customize

- **Add real APIs**: Replace simulated data with actual endpoints
- **Connect to database**: Add PostgreSQL/Snowflake connection
- **Add authentication**: Protect your dashboard
- **Customize theme**: Match your portfolio colors

See `README.md` for more details!

