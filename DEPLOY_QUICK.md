# Quick GitHub & Railway Deployment Script

## Step 1: Initialize Git and Push to GitHub

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - YouTube RAG Chat App ready for deployment"

# Add your GitHub repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/youtube-rag-chat.git

# Push to GitHub
git branch -M main
git push -u origin main

## Step 2: Deploy to Railway

1. Go to https://railway.app
2. Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Add environment variable:
   - Key: GEMINI_API_KEY
   - Value: your_actual_api_key
7. Deploy!

## That's it! Your app will be live at: https://your-app.up.railway.app
