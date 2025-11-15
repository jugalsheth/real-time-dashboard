# 🔒 Security Best Practices

## ✅ Security Checklist

### 1. **Never Commit Secrets**
- ✅ `.streamlit/secrets.toml` is in `.gitignore`
- ✅ Use `secrets.toml.example` as template
- ✅ Use Streamlit Cloud secrets for production

### 2. **Environment Variables**
- ✅ `.env` files are gitignored
- ✅ Use Streamlit secrets for sensitive data
- ✅ Never hardcode API keys in code

### 3. **Code Security**
- ✅ No credentials in source code
- ✅ All sensitive data uses `st.secrets`
- ✅ Input validation for user data

## 🔐 Setting Up Secrets

### Local Development

1. Copy the example file:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

2. Add your secrets to `.streamlit/secrets.toml`:
```toml
[api_keys]
github_token = "ghp_your_token_here"
```

3. Use in code:
```python
import streamlit as st

# Safe - uses secrets
token = st.secrets.get("api_keys", {}).get("github_token", None)
```

### Streamlit Cloud Deployment

1. Go to your app on Streamlit Cloud
2. Click "Settings" → "Secrets"
3. Add secrets in TOML format:
```toml
[api_keys]
github_token = "your_token_here"
database_url = "postgresql://..."
```

## 🚫 What NOT to Commit

- ❌ API keys or tokens
- ❌ Database passwords
- ❌ Private keys
- ❌ `.streamlit/secrets.toml`
- ❌ `.env` files
- ❌ Personal data

## ✅ Safe to Commit

- ✅ `secrets.toml.example` (template only)
- ✅ Code without hardcoded secrets
- ✅ Configuration files (without secrets)
- ✅ Documentation

## 🔍 Security Audit

Before pushing to GitHub, check:

```bash
# Search for potential secrets
grep -r "password\|token\|key\|secret" --include="*.py" | grep -v "#"
grep -r "api_key\|api_token" --include="*.py" | grep -v "#"

# Check gitignore
cat .gitignore

# Verify secrets.toml is ignored
git check-ignore .streamlit/secrets.toml
```

## 📚 Resources

- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

**Remember: If you accidentally commit secrets, rotate them immediately!**

