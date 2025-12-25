# 🎥 YouTube Video RAG Chat

An AI-powered chat application that lets you have intelligent conversations about YouTube videos using Retrieval Augmented Generation (RAG).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![Gemini](https://img.shields.io/badge/Gemini-API-orange.svg)

## ✨ Features

- 🎬 **Extract YouTube Transcripts** - Automatically fetches video captions
- 🧠 **RAG Technology** - Uses ChromaDB for intelligent context retrieval
- 💬 **Natural Language Q&A** - Ask questions in plain language
- 🌍 **Multi-language Support** - Works with Hindi, English, and other languages
- ⚡ **Smart Rate Limiting** - Optimized for free tier API quotas
- 🎨 **Modern UI** - Beautiful, responsive interface with dark theme

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one free](https://aistudio.google.com/apikey))

### Installation

1. **Clone or navigate to the project**
   ```bash
   cd e:\auto\youtube
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   python app.py
   ```
   
   You should see:
   ```
   * Running on http://127.0.0.1:5000
   ```

2. **Open the frontend**
   
   Double-click `index.html` or open it in your browser

3. **Start chatting!**
   - Paste a YouTube URL (with captions)
   - Click "Process Video"
   - Wait 3-5 minutes (rate limiting)
   - Ask questions about the video

## 📖 How It Works

```
YouTube Video → Transcript Extraction → Text Chunking → 
Vector Embeddings (Gemini) → ChromaDB Storage → 
User Question → Similarity Search → Context Retrieval → 
AI Response (Gemini)
```

1. **Transcript Extraction**: Fetches video captions using `youtube-transcript-api`
2. **Chunking**: Splits transcript into 500-word segments with 100-word overlap
3. **Embeddings**: Converts chunks to vectors using Gemini's `text-embedding-004`
4. **Storage**: Stores vectors in ChromaDB for fast retrieval
5. **Query**: Embeds your question and finds relevant video segments
6. **Response**: Gemini generates answers based on retrieved context

## 🎯 Usage Tips

### Choosing Videos
- ✅ Videos with auto-generated or manual captions
- ✅ Educational content, tutorials, talks
- ✅ Start with shorter videos (5-10 minutes)
- ❌ Avoid videos without captions
- ❌ Very long videos (1+ hour) take longer on free tier

### Processing Time
| Video Length | Chunks | Processing Time |
|--------------|--------|-----------------|
| 5 minutes    | 10-12  | 2-3 minutes     |
| 10 minutes   | 15-20  | 3-5 minutes     |
| 20 minutes   | 30-40  | 6-9 minutes     |

### Asking Questions
- Be specific: "What does the speaker say about X?"
- Reference topics: "Explain the concept mentioned at the beginning"
- Request summaries: "Summarize the main points"
- Ask for timestamps: "When is Y discussed?"

## 🌍 Language Support

The app supports multiple languages with this priority:
1. **Hindi** (`hi`) - Tried first
2. **English** (`en`) - Fallback
3. **Any available** - Uses whatever transcript exists

You can ask questions in any language, and Gemini will respond accordingly!

## ⚙️ Configuration

### API Rate Limits (Free Tier)

The app includes built-in rate limiting to stay within free tier quotas:
- **Delay**: 13 seconds between embedding requests
- **Model**: `gemini-2.5-flash` (10 RPM limit)
- **Embeddings**: `text-embedding-004`

### Environment Variables

Create a `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## 🐛 Troubleshooting

### "No transcript found"
- **Cause**: Video doesn't have captions
- **Solution**: Try a different video with captions enabled

### "API quota exceeded"
- **Cause**: Hit the rate limit
- **Solution**: Wait 1 minute and try again

### Port 5000 already in use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /F /PID <PID>

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Server won't start
- Check if `.env` file exists with valid API key
- Ensure all dependencies are installed
- Try reinstalling: `pip install -r requirements.txt --force-reinstall`

## 📁 Project Structure

```
youtube/
├── app.py              # Flask backend with RAG logic
├── index.html          # Frontend interface
├── style.css           # UI styling
├── script.js           # Frontend logic
├── requirements.txt    # Python dependencies
├── .env               # API key (create this)
├── .env.example       # Template for .env
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🔒 Security Notes

- ✅ `.env` file is gitignored (API key protected)
- ✅ CORS enabled for local development
- ⚠️ For production: restrict CORS, use HTTPS, add authentication

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **Vector Database**: ChromaDB
- **AI**: Google Gemini API
- **Transcript**: youtube-transcript-api
- **Frontend**: Vanilla HTML/CSS/JavaScript

## 📊 API Endpoints

### `POST /api/process-video`
Process a YouTube video and create embeddings
```json
{
  "url": "https://www.youtube.com/watch?v=..."
}
```

### `POST /api/chat`
Ask a question about the processed video
```json
{
  "video_id": "video_id",
  "question": "What is this video about?"
}
```

### `GET /api/health`
Health check endpoint

## 🎨 UI Features

- Modern dark theme with purple gradients
- Glassmorphism effects
- Smooth animations and transitions
- Responsive design (mobile + desktop)
- Typing indicators
- Word-wrapped messages
- User-friendly error messages

## 📈 Future Enhancements

- [ ] Video metadata display (title, thumbnail)
- [ ] Chat history export
- [ ] Multi-video support
- [ ] Auto-generated summaries
- [ ] Clickable timestamps
- [ ] Dark/Light mode toggle
- [ ] Caching processed videos

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 💡 Tips for Best Results

1. **Start small**: Test with 5-10 minute videos first
2. **Check captions**: Verify the video has captions on YouTube
3. **Be patient**: Processing takes time due to rate limiting
4. **Ask specific questions**: Better questions = better answers
5. **Use timestamps**: Reference specific parts of the video

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify your API key is valid
3. Ensure the video has captions
4. Check terminal output for detailed errors

---

**Made with ❤️ using Google Gemini AI**

**Star ⭐ this project if you find it useful!**
