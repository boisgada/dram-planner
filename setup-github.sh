#!/bin/bash
# Setup script for GitHub repository

GITHUB_USER="boisgada"
REPO_NAME="dram-planner"

echo "🚀 Setting up GitHub repository for dram-planner"
echo ""
echo "Repository will be: https://github.com/${GITHUB_USER}/${REPO_NAME}"
echo ""

# Check if remote already exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "⚠️  Remote 'origin' already exists:"
    git remote get-url origin
    echo ""
    read -p "Do you want to update it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote set-url origin "https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
        echo "✅ Remote updated"
    else
        echo "❌ Keeping existing remote"
        exit 1
    fi
else
    git remote add origin "https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
    echo "✅ Remote added"
fi

echo ""
echo "📋 Next steps:"
echo ""
echo "1. Create the repository on GitHub:"
echo "   Go to: https://github.com/new"
echo "   Repository name: ${REPO_NAME}"
echo "   Description: Plan your spirits tasting journey - A Python-based system for managing your spirits collection and creating structured tasting schedules"
echo "   Visibility: Public"
echo "   DO NOT initialize with README, .gitignore, or license (we already have them)"
echo "   Click 'Create repository'"
echo ""
echo "2. After creating the repository, run:"
echo "   git push -u origin main"
echo ""
echo "3. Create a release tag:"
echo "   git tag -a v0.1.0 -m 'Initial public release'"
echo "   git push origin v0.1.0"
echo ""

