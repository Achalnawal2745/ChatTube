// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// State
let currentVideoId = null;
let isProcessing = false;

// DOM Elements
const videoUrl = document.getElementById('videoUrl');
const processBtn = document.getElementById('processBtn');
const statusMessage = document.getElementById('statusMessage');
const videoInputSection = document.getElementById('videoInputSection');
const chatSection = document.getElementById('chatSection');
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const newVideoBtn = document.getElementById('newVideoBtn');

// Event Listeners
processBtn.addEventListener('click', processVideo);
sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
newVideoBtn.addEventListener('click', resetToNewVideo);

// Process Video
async function processVideo() {
    const url = videoUrl.value.trim();

    if (!url) {
        showStatus('Please enter a YouTube URL', 'error');
        return;
    }

    if (isProcessing) return;

    isProcessing = true;
    processBtn.disabled = true;

    // Show loading state
    processBtn.querySelector('.btn-text').style.display = 'none';
    processBtn.querySelector('.btn-loader').style.display = 'block';
    showStatus('Processing video... This may take a moment.', 'info');

    try {
        const response = await fetch(`${API_BASE_URL}/process-video`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to process video');
        }

        // Success
        currentVideoId = data.video_id;
        showStatus(`✓ Video processed successfully! Created ${data.chunks_created} knowledge chunks.`, 'success');

        // Show chat interface after a brief delay
        setTimeout(() => {
            videoInputSection.style.display = 'none';
            chatSection.style.display = 'flex';
            chatInput.focus();
        }, 1500);

    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        isProcessing = false;
        processBtn.disabled = false;
        processBtn.querySelector('.btn-text').style.display = 'inline';
        processBtn.querySelector('.btn-loader').style.display = 'none';
    }
}

// Send Chat Message
async function sendMessage() {
    const question = chatInput.value.trim();

    if (!question || !currentVideoId) return;

    // Add user message to chat
    addMessage(question, 'user');
    chatInput.value = '';

    // Show typing indicator
    const typingId = addTypingIndicator();

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                video_id: currentVideoId,
                question: question
            })
        });

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator(typingId);

        if (!response.ok) {
            throw new Error(data.error || 'Failed to get response');
        }

        // Add AI response
        addMessage(data.answer, 'ai');

    } catch (error) {
        removeTypingIndicator(typingId);

        // Format error message to be more user-friendly
        let errorMsg = error.message;

        // Check for quota errors
        if (errorMsg.includes('RESOURCE_EXHAUSTED') || errorMsg.includes('Quota exceeded')) {
            errorMsg = '⚠️ API quota exceeded. Please wait a few minutes or check your Gemini API quota limits at https://ai.google.dev/gemini-api/docs/rate-limits';
        } else if (errorMsg.length > 200) {
            // Truncate very long error messages
            errorMsg = errorMsg.substring(0, 200) + '... (error truncated)';
        }

        addMessage(`Sorry, I encountered an error: ${errorMsg}`, 'ai');
    }
}

// Add Message to Chat
function addMessage(text, sender) {
    // Remove welcome message if it exists
    const welcomeMsg = chatMessages.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? '👤' : '🤖';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.style.whiteSpace = 'pre-wrap';
    contentDiv.textContent = text;

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);

    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add Typing Indicator
function addTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ai typing-indicator';
    typingDiv.id = 'typing-' + Date.now();

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🤖';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = '<div class="typing-dots"><span>.</span><span>.</span><span>.</span></div>';

    // Add typing animation CSS if not already added
    if (!document.getElementById('typing-animation-style')) {
        const style = document.createElement('style');
        style.id = 'typing-animation-style';
        style.textContent = `
            .typing-dots {
                display: flex;
                gap: 4px;
            }
            .typing-dots span {
                animation: typingDot 1.4s infinite;
                opacity: 0.3;
            }
            .typing-dots span:nth-child(2) {
                animation-delay: 0.2s;
            }
            .typing-dots span:nth-child(3) {
                animation-delay: 0.4s;
            }
            @keyframes typingDot {
                0%, 60%, 100% { opacity: 0.3; }
                30% { opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }

    typingDiv.appendChild(avatar);
    typingDiv.appendChild(contentDiv);

    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return typingDiv.id;
}

// Remove Typing Indicator
function removeTypingIndicator(id) {
    const typingDiv = document.getElementById(id);
    if (typingDiv) {
        typingDiv.remove();
    }
}

// Show Status Message
function showStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
}

// Reset to New Video
function resetToNewVideo() {
    currentVideoId = null;
    videoUrl.value = '';
    chatMessages.innerHTML = `
        <div class="welcome-message">
            <div class="welcome-icon">💬</div>
            <h3>Ready to chat!</h3>
            <p>Ask me anything about this video</p>
        </div>
    `;
    chatSection.style.display = 'none';
    videoInputSection.style.display = 'block';
    statusMessage.className = 'status-message';
}
