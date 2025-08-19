#!/bin/bash

# Git Repository Setup Script
# This script helps you push your code to a remote repository

echo "🚀 Financial Data Processing System - Git Setup"
echo "================================================"
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository. Run 'git init' first."
    exit 1
fi

# Show current status
echo "📊 Current Repository Status:"
git log --oneline
echo ""

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Warning: You have uncommitted changes:"
    git status --short
    echo ""
    read -p "Do you want to commit these changes? (y/n): " commit_changes
    if [ "$commit_changes" = "y" ]; then
        git add .
        read -p "Enter commit message: " commit_msg
        git commit -m "$commit_msg"
        echo "✅ Changes committed!"
        echo ""
    fi
fi

# Instructions for GitHub
echo "🔗 To push to GitHub:"
echo "1. Go to https://github.com and create a new repository"
echo "2. Name it something like: 'financial-data-processor' or 'mongodb-ledger-system'"
echo "3. Don't initialize with README (we already have files)"
echo "4. Copy the repository URL (HTTPS or SSH)"
echo ""

# Get repository URL from user
read -p "📝 Enter your GitHub repository URL: " repo_url

if [ -n "$repo_url" ]; then
    echo ""
    echo "🔧 Setting up remote repository..."
    
    # Add remote origin
    git remote add origin "$repo_url" 2>/dev/null || {
        echo "⚠️  Remote 'origin' already exists. Updating URL..."
        git remote set-url origin "$repo_url"
    }
    
    # Push to repository
    echo "📤 Pushing to remote repository..."
    if git push -u origin master; then
        echo ""
        echo "🎉 Success! Your code has been pushed to GitHub!"
        echo "🌐 Repository URL: $repo_url"
        echo ""
        echo "📋 What's included in your repository:"
        echo "   ✅ MongoDB-based dynamic sub-ledger processor"
        echo "   ✅ Docker containerized setup"
        echo "   ✅ Complete documentation"
        echo "   ✅ Sample data and tests"
        echo "   ✅ Migration utilities"
        echo ""
        echo "🔍 Next steps:"
        echo "   • Clone the repository: git clone $repo_url"
        echo "   • Set up environment: docker-compose up -d"
        echo "   • Run processor: python3 dynamicSubLedger.py"
    else
        echo ""
        echo "❌ Push failed! Common solutions:"
        echo "   • Check your GitHub credentials"
        echo "   • Verify repository URL is correct"
        echo "   • Make sure you have push permissions"
        echo "   • Try: git push --set-upstream origin master"
    fi
else
    echo "⏭️  Skipping push setup. Your code is ready to push manually:"
    echo "   git remote add origin <your-repo-url>"
    echo "   git push -u origin master"
fi

echo ""
echo "📁 Repository contains $(git ls-files | wc -l) tracked files"
echo "💻 Total lines of code: $(git ls-files | grep -E '\.(py|js|yml|yaml|md)$' | xargs wc -l | tail -1)"
echo "🏷️  Latest commit: $(git log -1 --pretty=format:'%h - %s')"
