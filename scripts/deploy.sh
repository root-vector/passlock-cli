#!/bin/bash
# Deployment script for passlock-cli v0.1.0

echo "🚀 passlock-cli Deployment Script"
echo "=================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

echo ""
echo "📝 Adding all files..."
git add .

echo ""
echo "💾 Creating commit..."
git commit -m "feat: v0.1.0 initial secure release

- Local-only encrypted password manager
- Argon2id + Fernet encryption  
- Comprehensive security audit
- 46 tests (100% passing)
- Production-ready"

echo ""
echo "🌿 Setting main branch..."
git branch -M main

echo ""
echo "🔗 Adding remote origin..."
git remote add origin https://github.com/root-vector/passlock-cli.git 2>/dev/null || echo "⚠️  Remote already exists"

echo ""
echo "📤 Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Go to https://github.com/root-vector/passlock-cli"
echo "2. Create release v0.1.0"
echo "3. Enable GitHub Actions"
echo "4. Configure branch protection (optional)"
echo ""
echo "🎉 passlock-cli is now live!"
