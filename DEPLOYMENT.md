# YouTube RAG Chat - Railway Deployment Guide

## 🚀 Complete Deployment Guide

### Prerequisites
- GitHub account
- Railway account (sign up at [railway.app](https://railway.app))
- Your Gemini API key

---

## 📋 Step 1: Prepare for GitHub

### 1.1 Initialize Git (if not already done)
```bash
cd e:\auto\youtube
git init
```

### 1.2 Create .gitignore (already exists)
Make sure `.env` is in `.gitignore` - ✅ Already done!

### 1.3 Commit Your Code
```bash
git add .
git commit -m "Initial commit - YouTube RAG Chat App"
```

### 1.4 Create GitHub Repository
1. Go to [github.com](https://github.com)
2. Click "New Repository"
3. Name it: `youtube-rag-chat`
4. Don't initialize with README (we already have files)
5. Click "Create Repository"

### 1.5 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/youtube-rag-chat.git
git branch -M main
git push -u origin main
```

---

## 🚂 Step 2: Deploy to Railway

### 2.1 Sign Up for Railway
1. Go to [railway.app](https://railway.app)
2. Click "Login" → "Login with GitHub"
3. Authorize Railway to access your GitHub

### 2.2 Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `youtube-rag-chat` repository
4. Railway will auto-detect it's a Python app

### 2.3 Configure Environment Variables
1. In your Railway project, click on your service
2. Go to "Variables" tab
3. Add this variable:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
4. Click "Add Variable"

### 2.4 Wait for Deployment
- Railway will automatically:
  - Install dependencies from `requirements.txt`
  - Run your app using `Procfile`
  - Assign a public URL

### 2.5 Get Your URL
- Once deployed, you'll see a URL like: `https://your-app.up.railway.app`
- Click it to open your app!

---

## ✅ Step 3: Test Your Deployment

1. **Open the Railway URL** in your browser
2. **Paste a YouTube URL** (with captions)
3. **Click "Process Video"**
4. **Wait for processing** (3-5 minutes)
5. **Start chatting!**

---

## 🔧 Troubleshooting

### App Not Loading?
**Check Railway Logs:**
1. Go to your Railway project
2. Click "Deployments" tab
3. Click latest deployment
4. Check logs for errors

### Common Issues:

#### "GEMINI_API_KEY not found"
- ✅ Add it in Railway Variables tab
- ✅ Redeploy after adding

#### "No module named 'gunicorn'"
- ✅ Make sure `requirements.txt` includes `gunicorn>=21.2.0`
- ✅ Redeploy

#### ChromaDB Issues
- ✅ Railway has persistent storage - should work fine
- ✅ Check logs for specific errors

---

## 💰 Railway Free Tier Info

### What You Get:
- ✅ **$5 free credit** (no credit card needed)
- ✅ **Persistent storage** (ChromaDB works!)
- ✅ **No sleep** (stays active)
- ✅ **500 GB bandwidth**

### How Long Does $5 Last?
- **~1 month** of continuous running
- **Longer** if not used 24/7

### After Free Credit Runs Out:
- ⚠️ App will stop
- ✅ Can add credit card to continue
- ✅ Or delete and redeploy (new $5 credit)

---

## 🔄 Updating Your App

### Make Changes Locally:
```bash
# Make your code changes
git add .
git commit -m "Updated feature X"
git push
```

### Railway Auto-Deploys:
- ✅ Railway watches your GitHub repo
- ✅ Automatically redeploys on push
- ✅ No manual steps needed!

---

## 🛑 Stopping/Deleting

### To Pause:
1. Go to Railway project
2. Click service
3. Click "Settings"
4. Click "Remove Service"

### To Delete Completely:
1. Go to Railway dashboard
2. Click project
3. Click "Settings"
4. Scroll down → "Delete Project"

---

## 📊 Monitoring

### Check Usage:
1. Railway Dashboard → Your Project
2. See metrics: CPU, Memory, Network
3. Track your $5 credit usage

### View Logs:
1. Click "Deployments"
2. Click latest deployment
3. See real-time logs

---

## 🎯 Production Checklist

Before sharing your app:
- [ ] Test with multiple videos
- [ ] Test in different browsers
- [ ] Check API quota limits
- [ ] Monitor Railway usage
- [ ] Set up error monitoring (optional)

---

## 🔐 Security Notes

### Environment Variables:
- ✅ Never commit `.env` to GitHub
- ✅ Use Railway Variables for API keys
- ✅ Rotate API keys periodically

### CORS:
- ⚠️ Currently allows all origins
- 🔒 For production, restrict to your domain:
  ```python
  CORS(app, origins=["https://your-app.up.railway.app"])
  ```

---

## 📞 Support

### Railway Issues:
- [Railway Discord](https://discord.gg/railway)
- [Railway Docs](https://docs.railway.app)

### App Issues:
- Check Railway logs
- Check Gemini API quota
- Verify environment variables

---

## 🎉 You're Done!

Your YouTube RAG Chat app is now live and accessible to anyone with the URL!

**Share your app:** `https://your-app.up.railway.app`

---

## 📝 Quick Reference

### Local Development:
```bash
python app.py
# Open http://localhost:5000
```

### Deploy Updates:
```bash
git add .
git commit -m "Your message"
git push
# Railway auto-deploys!
```

### Check Logs:
Railway Dashboard → Deployments → Latest → Logs

### Environment Variables:
Railway Dashboard → Variables → Add Variable
