# 🚀 Deployment Guide - Real-Time Analytics Dashboard

## Quick Deploy Options

### Option 1: Streamlit Cloud (Recommended - Free & Easy)

1. **Push to GitHub**
   ```bash
   cd real-time-dashboard
   git init
   git add .
   git commit -m "Initial commit: Real-time analytics dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/real-time-dashboard.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository and branch
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Update Portfolio**
   - Copy your Streamlit Cloud URL (e.g., `https://your-app.streamlit.app`)
   - Update `src/portfolio.js`:
     ```javascript
     embedUrl: "https://your-app.streamlit.app"
     ```

### Option 2: Railway (Free Tier Available)

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   ```

2. **Deploy**
   ```bash
   cd real-time-dashboard
   railway login
   railway init
   railway up
   ```

3. **Add Procfile** (if needed)
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

### Option 3: Render

1. Create new Web Service on Render
2. Connect GitHub repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `streamlit run app.py --server.port=$PORT`
5. Add environment variable: `PORT=8501`

### Option 4: Heroku

1. **Create Procfile**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy**
   ```bash
   heroku create your-dashboard-name
   git push heroku main
   ```

## Testing Locally

```bash
cd real-time-dashboard
pip install -r requirements.txt
streamlit run app.py
```

Visit: `http://localhost:8501`

## Customization

### Add Real Data Sources

Replace simulated data in `app.py`:

```python
def fetch_real_data():
    # Example: GitHub API
    response = requests.get("https://api.github.com/users/jugalsheth/events")
    data = response.json()
    # Process and return metrics
    return processed_metrics
```

### Connect to Actual Pipeline

```python
# Example: Connect to Kafka/Redis/PostgreSQL
import redis
r = redis.Redis(host='localhost', port=6379)
metrics = r.get('pipeline_metrics')
```

### Add Authentication

```python
# In app.py
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    credentials,
    'dashboard_cookie',
    'dashboard_key',
    cookie_expiry_days=30
)
```

## Troubleshooting

**Issue**: Dashboard not loading in iframe
- **Solution**: Add to Streamlit config:
  ```toml
  [server]
  enableXsrfProtection = false
  ```

**Issue**: CORS errors
- **Solution**: Streamlit Cloud handles this automatically

**Issue**: Slow loading
- **Solution**: Optimize data fetching, add caching:
  ```python
  @st.cache_data(ttl=60)
  def fetch_data():
      # Your data fetching logic
  ```

## Next Steps

1. ✅ Deploy to Streamlit Cloud
2. ✅ Update portfolio.js with your URL
3. ✅ Test embedded dashboard in portfolio
4. 🔄 Add real data sources
5. 🔄 Implement authentication
6. 🔄 Add database persistence

---

**Need help?** Check Streamlit docs: [docs.streamlit.io](https://docs.streamlit.io)

