# 🚀 Running the Dashboard Locally

## Quick Start

Since `pip` and `streamlit` commands might not be in your PATH, use these commands:

### Install Dependencies
```bash
cd real-time-dashboard
python3 -m pip install -r requirements.txt
```

### Run the Dashboard
```bash
python3 -m streamlit run app.py
```

The dashboard will open at: **http://localhost:8501**

## Alternative: Add to PATH (Optional)

If you want to use `streamlit` directly, add Python scripts to your PATH:

```bash
# Add to ~/.zshrc (or ~/.bash_profile for bash)
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
```

Then reload:
```bash
source ~/.zshrc
```

Now you can use:
```bash
streamlit run app.py
```

## Troubleshooting

**Issue**: `python3 -m streamlit` not found
- **Solution**: Make sure Streamlit is installed:
  ```bash
  python3 -m pip install streamlit
  ```

**Issue**: Port 8501 already in use
- **Solution**: Use a different port:
  ```bash
  python3 -m streamlit run app.py --server.port 8502
  ```

---

**Note**: For deployment, you don't need these commands - Streamlit Cloud handles everything automatically!

