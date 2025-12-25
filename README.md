# YouTube RAG Chat 🎥💬

An AI-powered chat application that lets you have conversations about YouTube videos using Retrieval Augmented Generation (RAG).

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🎬 **YouTube Transcript Extraction** - Automatically extracts video transcripts
- 🧠 **RAG Technology** - Uses ChromaDB for intelligent context retrieval
- 💬 **AI Chat** - Powered by Google Gemini for natural conversations
- 🌍 **Multi-language Support** - Works with Hindi, English, and other languages
- ⚡ **Fast & Accurate** - Retrieves relevant video segments for precise answers
- 🎨 **Modern UI** - Beautiful, responsive interface with smooth animations

## 🚀 Live Demo

[Your Railway URL will go here after deployment]

## 📸 Screenshots

[Add screenshots of your app here]

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Vector Database**: ChromaDB
- **AI**: Google Gemini API
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Deployment**: Railway

## 📋 Prerequisites

- Python 3.11+
- Google Gemini API Key ([Get one here](https://aistudio.google.com/apikey))

## 🏃 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/youtube-rag-chat.git
cd youtube-rag-chat
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the Application
```bash
python app.py
```

### 5. Open in Browser
Navigate to `http://localhost:5000`

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed Railway deployment instructions.

## 📖 How It Works

1. **Extract**: Gets video transcript with timestamps
2. **Chunk**: Splits transcript into overlapping segments
3. **Embed**: Converts chunks to vectors using Gemini
4. **Store**: Saves embeddings in ChromaDB
5. **Query**: Finds relevant chunks for user questions
6. **Generate**: Creates answers using Gemini with context

## 🎯 Usage

1. Paste a YouTube video URL (must have captions)
2. Click "Process Video" (takes 3-5 minutes)
3. Ask questions about the video
4. Get AI-powered answers with timestamp references

## ⚙️ Configuration

### API Rate Limits
Free tier includes 13-second delays between requests to stay within Gemini API limits.

### Supported Languages
- Hindi (hi)
- English (en)
- Any language with available YouTube transcripts

## 🐛 Troubleshooting

### "No transcript found"
- Ensure the video has captions/subtitles enabled
- Try a different video

### "API quota exceeded"
- Wait a few minutes
- Check your Gemini API quota at [ai.google.dev](https://ai.google.dev)

### Slow processing
- Normal for free tier (rate limiting)
- Shorter videos process faster

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 👨‍💻 Author

[Your Name]

## 🙏 Acknowledgments

- Google Gemini API
- ChromaDB
- YouTube Transcript API
- Flask Framework

## 📧 Contact

[Your contact information]

---

⭐ Star this repo if you found it helpful!
