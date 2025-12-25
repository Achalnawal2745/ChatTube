from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from google import genai
from google.genai import types
import chromadb
from chromadb.config import Settings
import os
from dotenv import load_dotenv
import re
from urllib.parse import urlparse, parse_qs
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API (only for chat, not embeddings)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please create a .env file with your API key.")

client = genai.Client(api_key=GEMINI_API_KEY)

# Initialize Sentence Transformer for local embeddings
print("Loading Sentence Transformer model...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded successfully!")

# Initialize ChromaDB
chroma_client = chromadb.Client(Settings(
    persist_directory="./chroma_db",
    anonymized_telemetry=False
))

# Store for video sessions
video_sessions = {}


def extract_video_id(url):
    """Extract YouTube video ID from URL"""
    parsed_url = urlparse(url)
    
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query).get('v', [None])[0]
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    
    return None


def chunk_transcript(transcript, chunk_size=500, overlap=100):
    """Split transcript into overlapping chunks"""
    chunks = []
    text_parts = []
    
    for entry in transcript:
        text_parts.append({
            'text': entry['text'],
            'start': entry['start']
        })
    
    # Combine into chunks
    current_chunk = []
    current_length = 0
    
    for i, part in enumerate(text_parts):
        words = part['text'].split()
        current_chunk.extend(words)
        current_length += len(words)
        
        if current_length >= chunk_size:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'text': chunk_text,
                'start_time': text_parts[max(0, i - len(current_chunk) + 1)]['start']
            })
            
            # Keep overlap for next chunk
            current_chunk = current_chunk[-overlap:] if len(current_chunk) > overlap else []
            current_length = len(current_chunk)
    
    # Add remaining text
    if current_chunk:
        chunks.append({
            'text': ' '.join(current_chunk),
            'start_time': text_parts[-1]['start']
        })
    
    return chunks


@app.route('/api/process-video', methods=['POST'])
def process_video():
    """Process YouTube video and create embeddings"""
    try:
        data = request.json
        video_url = data.get('url')
        
        if not video_url:
            return jsonify({'error': 'No URL provided'}), 400
        
        # Extract video ID
        video_id = extract_video_id(video_url)
        if not video_id:
            return jsonify({'error': 'Invalid YouTube URL'}), 400
        
        # Get transcript
        try:
            api = YouTubeTranscriptApi()
            
            # Try to get transcript in multiple languages
            # Priority: Hindi, English, then any available
            try:
                # Try Hindi first
                transcript_data = api.fetch(video_id, languages=['hi'])
            except:
                try:
                    # Try English
                    transcript_data = api.fetch(video_id, languages=['en'])
                except:
                    # Try any available language
                    transcript_list = api.list(video_id)
                    # Get the first available transcript
                    available_transcripts = list(transcript_list)
                    if available_transcripts:
                        first_transcript = available_transcripts[0]
                        transcript_data = api.fetch(video_id, languages=[first_transcript.language_code])
                    else:
                        raise NoTranscriptFound("No transcripts available")
            
            # Convert snippets to the expected format
            transcript = [{'text': snippet.text, 'start': snippet.start} for snippet in transcript_data.snippets]
        except TranscriptsDisabled:
            return jsonify({'error': 'Transcripts are disabled for this video'}), 400
        except NoTranscriptFound:
            return jsonify({'error': 'No transcript found for this video. Please try a video with captions/subtitles.'}), 400
        except Exception as e:
            return jsonify({'error': f'Error fetching transcript: {str(e)}'}), 400
        
        # Chunk the transcript
        chunks = chunk_transcript(transcript)
        
        # Create or get collection for this video
        collection_name = f"video_{video_id}"
        try:
            chroma_client.delete_collection(collection_name)
        except:
            pass
        
        collection = chroma_client.create_collection(
            name=collection_name,
            metadata={"video_id": video_id}
        )
        
        # Generate embeddings and store in ChromaDB
        texts = [chunk['text'] for chunk in chunks]
        metadatas = [{'start_time': chunk['start_time']} for chunk in chunks]
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        
        # Use local Sentence Transformer for embeddings (MUCH faster!)
        print(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = embedding_model.encode(texts, show_progress_bar=True).tolist()
        print("Embeddings generated successfully!")
        
        collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        # Store session info
        video_sessions[video_id] = {
            'collection_name': collection_name,
            'total_chunks': len(chunks)
        }
        
        return jsonify({
            'success': True,
            'video_id': video_id,
            'chunks_created': len(chunks),
            'message': 'Video processed successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat queries about the video"""
    try:
        data = request.json
        video_id = data.get('video_id')
        question = data.get('question')
        
        if not video_id or not question:
            return jsonify({'error': 'Missing video_id or question'}), 400
        
        if video_id not in video_sessions:
            return jsonify({'error': 'Video not processed yet'}), 400
        
        # Get collection
        collection_name = video_sessions[video_id]['collection_name']
        collection = chroma_client.get_collection(collection_name)
        
        # Generate query embedding using local model (instant!)
        query_embedding = embedding_model.encode([question])[0].tolist()
        
        # Retrieve relevant chunks
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )
        
        # Build context from retrieved chunks
        context_parts = []
        for i, doc in enumerate(results['documents'][0]):
            timestamp = results['metadatas'][0][i]['start_time']
            context_parts.append(f"[{int(timestamp)}s] {doc}")
        
        context = "\n\n".join(context_parts)
        
        # Generate response using Gemini
        prompt = f"""You are a helpful assistant that answers questions about a YouTube video based on its transcript.

Context from the video (with timestamps in seconds):
{context}

User question: {question}

Please provide a helpful answer based on the context above. If you reference specific information, mention the approximate timestamp. If the context doesn't contain enough information to answer the question, say so politely."""
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        return jsonify({
            'success': True,
            'answer': response.text,
            'sources': [{'timestamp': meta['start_time']} for meta in results['metadatas'][0]]
        })
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Chat error: {str(e)}")
        print(f"Full traceback:\n{error_details}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
