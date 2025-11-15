#!/bin/bash

# Deployment script for Real-Time Analytics Dashboard
# This script helps you safely deploy to GitHub and Streamlit Cloud

set -e  # Exit on error

echo "🚀 Real-Time Dashboard Deployment Script"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ Error: app.py not found. Please run this script from the real-time-dashboard directory.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Step 1: Security Checks${NC}"
echo "Checking for secrets..."

# Check if secrets.toml exists (should NOT be committed)
if [ -f ".streamlit/secrets.toml" ]; then
    echo -e "${YELLOW}⚠️  Warning: .streamlit/secrets.toml exists locally (this is OK for local dev)${NC}"
    if git check-ignore .streamlit/secrets.toml > /dev/null 2>&1; then
        echo -e "${GREEN}✅ secrets.toml is properly ignored by git${NC}"
    else
        echo -e "${RED}❌ ERROR: secrets.toml is NOT in .gitignore!${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ No secrets.toml found (using example template)${NC}"
fi

# Check for hardcoded secrets in code
echo "Scanning for potential hardcoded secrets..."
if grep -r "password\s*=\s*['\"].*['\"]" --include="*.py" | grep -v "#" | grep -v "example" | grep -v "secrets.toml.example"; then
    echo -e "${YELLOW}⚠️  Warning: Potential hardcoded passwords found. Please review.${NC}"
else
    echo -e "${GREEN}✅ No hardcoded secrets found${NC}"
fi

echo ""
echo -e "${GREEN}✅ Step 2: Git Status${NC}"
git status --short

echo ""
echo -e "${GREEN}✅ Step 3: Ready to Deploy${NC}"
echo ""
echo "Next steps:"
echo "1. Review the files above"
echo "2. Run: git add ."
echo "3. Run: git commit -m 'Initial commit: Real-time analytics dashboard'"
echo "4. Create GitHub repo and push:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/real-time-dashboard.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "5. Deploy to Streamlit Cloud:"
echo "   - Go to https://share.streamlit.io"
echo "   - Connect your GitHub repo"
echo "   - Deploy!"
echo ""
echo -e "${GREEN}📚 See DEPLOY_TO_STREAMLIT.md for detailed instructions${NC}"

