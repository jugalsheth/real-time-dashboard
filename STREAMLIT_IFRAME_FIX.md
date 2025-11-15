# 🔧 Streamlit Iframe Embedding Fix

## Issue
Streamlit Cloud may block iframe embedding by default due to security headers.

## Solution

### Option 1: Streamlit Cloud Settings (Recommended)

1. Go to your Streamlit Cloud app: https://real-time-dashboard-vjf78bbxheqjjwefbgutyw.streamlit.app
2. Click on the **Settings** (⚙️) icon
3. Go to **Advanced settings**
4. Under **Security**, make sure:
   - "Enable XSRF protection" is **OFF** (for iframe embedding)
   - Or add your portfolio domain to allowed origins

### Option 2: Update Streamlit Config

The `.streamlit/config.toml` has been updated with:
```toml
[server]
enableXsrfProtection = false
```

**Note**: This needs to be deployed to Streamlit Cloud. Push the updated config:

```bash
cd real-time-dashboard
git add .streamlit/config.toml
git commit -m "Enable iframe embedding"
git push
```

### Option 3: Use Streamlit's Embed Feature

Streamlit Cloud has a built-in embed feature. You can:
1. Go to your app settings
2. Enable "Allow embedding"
3. Use the embed URL format if available

## Testing Locally

The iframe should work locally at `localhost:3000`. If it doesn't load:

1. **Check browser console** for errors
2. **Check Network tab** to see if the request is blocked
3. **Try opening the Streamlit URL directly** to verify it's working

## Common Issues

### Issue: "Refused to display in a frame"
**Solution**: Streamlit Cloud needs XSRF protection disabled or your domain whitelisted

### Issue: Blank iframe
**Solution**: 
- Check if Streamlit app is running
- Verify URL is correct
- Check browser console for CORS errors

### Issue: Iframe loads but is blank
**Solution**: 
- Streamlit might need a moment to load
- Check if there are JavaScript errors
- Try increasing iframe height

## Current Implementation

The portfolio now includes:
- ✅ Sandbox attributes for security
- ✅ Fallback link to open in new tab
- ✅ Error handling
- ✅ Proper iframe attributes

## Next Steps

1. **Push config update** to Streamlit Cloud (if needed)
2. **Test locally** - should work at localhost:3000
3. **Deploy portfolio** - will work the same in production

---

**The iframe should work both locally and in production!** 🚀

