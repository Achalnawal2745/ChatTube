# Quick Setup Guide

## ✅ Code Updated!

The application has been updated to use the new `google-genai` package (the old `google-generativeai` is deprecated).

## 🔑 Next Step: Add Your API Key

You need to add your Gemini API key to the `.env` file:

### Option 1: Edit the existing .env file
Open `e:\auto\youtube\.env` and make sure it contains:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### Option 2: Create .env file from scratch
If you don't have a `.env` file yet, create one with:
```
GEMINI_API_KEY=your_actual_api_key_here
```

## 🔗 Get Your API Key

1. Visit: https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy the key
4. Paste it in your `.env` file (replace `your_actual_api_key_here`)

## ▶️ Run the Application

Once you've added your API key:

```bash
python app.py
```

The server will start at `http://localhost:5000`

Then open `index.html` in your browser!

## 📝 What Changed

- ✅ Updated from `google-generativeai` → `google-genai` (new package)
- ✅ Updated embedding model to `text-embedding-004` (latest)
- ✅ Updated chat model to `gemini-2.0-flash-exp` (latest)
- ✅ Installed new package automatically
- ✅ Better error message for missing API key

## ⚠️ Important

Make sure your `.env` file:
- Is in the `e:\auto\youtube\` directory
- Contains `GEMINI_API_KEY=your_key` (no quotes, no spaces around =)
- Has your actual API key (not the example text)
