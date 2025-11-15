# 📊 Real-Time Analytics Dashboard

A production-ready real-time analytics dashboard for monitoring data pipelines, system metrics, and live data streams.

## 🔒 Security

This repository follows security best practices:
- ✅ No secrets committed to git
- ✅ Uses Streamlit Cloud secrets for sensitive data
- ✅ All API keys stored securely
- See [SECURITY.md](./SECURITY.md) for details

## 🚀 Features

- **Real-Time Updates** - Live data streaming with configurable refresh intervals
- **Multiple Data Sources** - Support for simulated pipelines, GitHub activity, stock prices, and more
- **Interactive Charts** - Beautiful Plotly visualizations with gauges, heatmaps, and multi-pipeline views
- **Anomaly Detection** - Z-score based statistical anomaly detection
- **Alert System** - Configurable thresholds with visual alerts
- **Key Metrics** - Throughput, latency (P95/P99), success rate, data quality, and system resources
- **Data Export** - CSV and JSON export functionality
- **Responsive Design** - Works on all devices

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas
- **APIs**: Requests (for external data sources)

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 🌐 Deployment

### Streamlit Cloud (Recommended - Free)

1. Push this folder to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub repo
4. Select this folder
5. Deploy!

### Other Options

- **Heroku**: Add `Procfile` with `web: streamlit run app.py --server.port=$PORT`
- **Railway**: Connect GitHub repo, auto-detects Streamlit
- **Render**: Add web service, use `streamlit run app.py`

## 🔗 Embedding in Portfolio

Once deployed, embed in your portfolio:

```html
<iframe 
  src="https://your-app.streamlit.app" 
  width="100%" 
  height="700px"
  frameborder="0"
  scrolling="no"
></iframe>
```

Or add to `portfolio.js`:

```javascript
{
  projectName: "Real-Time Analytics Dashboard",
  projectDesc: "Live monitoring dashboard for data pipelines with real-time metrics and visualizations",
  embedUrl: "https://your-app.streamlit.app",
  footerLink: [
    { name: "Live Demo", url: "https://your-app.streamlit.app" },
    { name: "GitHub", url: "https://github.com/yourusername/repo" }
  ]
}
```

## 🎨 Customization

- **Add Real APIs**: Replace simulated data with actual API calls
- **Custom Metrics**: Add your own KPIs
- **Themes**: Customize colors in the CSS section
- **Data Sources**: Add more data sources (Twitter, Reddit, etc.)

## 📈 Next Steps

1. Add real API integrations
2. Connect to actual data pipelines
3. Add authentication for production use
4. Implement data persistence (database)
5. Add alerting/notifications

---

**Built by Jugal Sheth | Data Engineer**

