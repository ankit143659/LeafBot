import streamlit as st
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Academic AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Global styles */
    .main {
        padding: 0rem 1rem;
    }
    
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Sidebar styling - professional light theme */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E8F5E9;
        padding: 2rem 1rem;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 0rem;
    }
    
    /* Chat history panel */
    .chat-history-item {
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 0.9rem;
        color: #2E7D32;
        border-left: 3px solid transparent;
    }
    
    .chat-history-item:hover {
        background-color: #F1F8E9;
        border-left: 3px solid #4CAF50;
    }
    
    .chat-history-item.active {
        background-color: #E8F5E9;
        border-left: 3px solid #2E7D32;
        font-weight: 500;
    }
    
    /* User profile section */
    .user-profile {
        position: absolute;
        bottom: 2rem;
        left: 1rem;
        right: 1rem;
        padding: 1rem;
        border-top: 1px solid #E8F5E9;
    }
    
    .user-name {
        font-weight: 600;
        color: #2E7D32;
        font-size: 0.95rem;
    }
    
    /* Main chat area */
    .chat-container {
        display: flex;
        flex-direction: column;
        height: calc(100vh - 120px);
        padding-bottom: 80px;
        overflow-y: auto;
    }
    
    /* Message bubbles */
    .user-message {
        background-color: #E8F5E9;
        color: #1B5E20;
        padding: 1rem 1.25rem;
        border-radius: 18px 18px 4px 18px;
        margin: 0.5rem 0;
        max-width: 70%;
        align-self: flex-end;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        border: 1px solid #C8E6C9;
    }
    
    .assistant-message {
        background-color: #FFFFFF;
        color: #37474F;
        padding: 1rem 1.25rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.5rem 0;
        max-width: 70%;
        align-self: flex-start;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #F5F5F5;
    }
    
    /* Input area - fixed at bottom */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 1rem 2rem;
        border-top: 1px solid #E8F5E9;
        z-index: 100;
    }
    
    /* Custom text input */
    .stTextInput > div > div > input {
        border-radius: 24px;
        border: 1px solid #C8E6C9;
        padding: 0.75rem 1.25rem;
        font-size: 0.95rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 1px #4CAF50;
    }
    
    /* Custom button styling */
    .new-chat-btn {
        background-color: #4CAF50 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        width: 100% !important;
        margin-bottom: 1.5rem !important;
    }
    
    .new-chat-btn:hover {
        background-color: #388E3C !important;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F5F5F5;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #C8E6C9;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #A5D6A7;
    }
    
    /* Typography */
    .chat-title {
        font-size: 0.85rem;
        font-weight: 500;
        color: #2E7D32;
        margin-bottom: 0.25rem;
    }
    
    .chat-preview {
        font-size: 0.8rem;
        color: #666;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .message-time {
        font-size: 0.75rem;
        color: #888;
        margin-top: 0.25rem;
        text-align: right;
    }
    
    .assistant-time {
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    
if 'current_chat' not in st.session_state:
    st.session_state.current_chat = []
    
if 'chat_counter' not in st.session_state:
    st.session_state.chat_counter = 0

# Function to create new chat
def new_chat():
    if st.session_state.current_chat:
        # Save current chat to history
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        preview = st.session_state.current_chat[0]['content'][:50] + "..." if st.session_state.current_chat[0]['content'] else "New chat"
        st.session_state.chat_history.append({
            'id': st.session_state.chat_counter,
            'title': f"Chat {st.session_state.chat_counter + 1}",
            'preview': preview,
            'timestamp': timestamp,
            'messages': st.session_state.current_chat.copy()
        })
        st.session_state.chat_counter += 1
    
    # Clear current chat
    st.session_state.current_chat = []
    st.rerun()

# Function to load chat from history
def load_chat(chat_id):
    for chat in st.session_state.chat_history:
        if chat['id'] == chat_id:
            st.session_state.current_chat = chat['messages']
            st.rerun()
            break

# Function to simulate AI response
def get_ai_response(user_message):
    # Simulate AI processing delay
    time.sleep(0.5)
    
    # Sample academic-focused responses
    responses = [
        "Based on your query about machine learning algorithms, I recommend exploring decision trees and random forests for your classification task. These algorithms provide good interpretability while maintaining high accuracy.",
        "For your database design project, consider implementing a normalized schema up to 3NF to reduce data redundancy while maintaining query performance through proper indexing strategies.",
        "In software engineering methodologies, Agile practices combined with DevOps principles can significantly improve your project delivery timeline and code quality metrics.",
        "Regarding your cybersecurity concerns, implementing multi-factor authentication and regular security audits should be prioritized in your network architecture design.",
        "For your cloud computing project, AWS offers a comprehensive free tier that includes EC2 instances, S3 storage, and RDS databases suitable for academic prototypes."
    ]
    
    import random
    return random.choice(responses)

# Sidebar - Chat History Panel
with st.sidebar:
    # Professional header
    st.markdown("<h3 style='color: #2E7D32; margin-bottom: 2rem;'>Chat History</h3>", unsafe_allow_html=True)
    
    # New Chat button
    if st.button("＋ New Chat", key="new_chat", use_container_width=True, 
                 type="primary", help="Start a new conversation"):
        new_chat()
    
    st.markdown("---")
    
    # Chat history list
    if st.session_state.chat_history:
        st.markdown("<p style='color: #666; font-size: 0.9rem; margin-bottom: 1rem;'>Recent Conversations</p>", unsafe_allow_html=True)
        
        # Display chats in reverse chronological order (newest first)
        for chat in reversed(st.session_state.chat_history):
            is_active = any(msg['content'] for msg in chat['messages']) and st.session_state.current_chat == chat['messages']
            active_class = "active" if is_active else ""
            
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.markdown(f"""
                <div class='chat-history-item {active_class}' onclick='window.parent.streamlitApi.runMethod("load_chat", {chat["id"]})'>
                    <div class='chat-title'>{chat['title']}</div>
                    <div class='chat-preview'>{chat['preview']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.caption(chat['timestamp'].split()[0])
    else:
        st.markdown("<p style='color: #888; font-size: 0.9rem; text-align: center; padding: 2rem;'>No chat history yet</p>", unsafe_allow_html=True)
    
    # User profile section at bottom
    st.markdown("<div class='user-profile'>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div class='user-name'>Student ID: MCA2024001</div>", unsafe_allow_html=True)
    st.markdown("<div style='color: #666; font-size: 0.85rem;'>Academic AI Assistant v2.1</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Main Chat Window
st.markdown("<h1 style='color: #2E7D32; margin-bottom: 1.5rem;'>Academic AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #666; margin-bottom: 2rem;'>Professional AI assistant for academic research and project guidance</p>", unsafe_allow_html=True)

# Chat container
chat_container = st.container()

with chat_container:
    st.markdown("<div class='chat-container' id='chat-container'>", unsafe_allow_html=True)
    
    # Display current chat messages
    for i, message in enumerate(st.session_state.current_chat):
        if message['role'] == 'user':
            st.markdown(f"""
            <div class='user-message'>
                {message['content']}
                <div class='message-time'>{message.get('timestamp', '')}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='assistant-message'>
                {message['content']}
                <div class='message-time assistant-time'>{message.get('timestamp', '')}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Display welcome message if no chat history
    if not st.session_state.current_chat:
        st.markdown("""
        <div style='text-align: center; padding: 3rem; color: #888;'>
            <h3 style='color: #2E7D32; margin-bottom: 1rem;'>Welcome to Academic AI Assistant</h3>
            <p>Start a new conversation by typing your message below.</p>
            <p style='font-size: 0.9rem; margin-top: 2rem;'>Try asking about:</p>
            <p style='font-size: 0.85rem; color: #666;'>
                • Machine learning algorithms for classification<br>
                • Database normalization techniques<br>
                • Software engineering methodologies<br>
                • Cloud computing architecture patterns<br>
                • Cybersecurity best practices
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Fixed input area at bottom
st.markdown("<div class='input-container'>", unsafe_allow_html=True)

col1, col2 = st.columns([0.9, 0.1])

with col1:
    user_input = st.text_input(
        "Type your message...",
        key="user_input",
        label_visibility="collapsed",
        placeholder="Ask about academic topics, project guidance, or research methodologies..."
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    send_button = st.button("➤", use_container_width=True, type="primary")

# Handle message sending
if send_button and user_input:
    # Add user message to current chat
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.current_chat.append({
        'role': 'user',
        'content': user_input,
        'timestamp': timestamp
    })
    
    # Get AI response
    with st.spinner("Processing..."):
        ai_response = get_ai_response(user_input)
    
    # Add AI response to current chat
    st.session_state.current_chat.append({
        'role': 'assistant',
        'content': ai_response,
        'timestamp': datetime.now().strftime("%H:%M")
    })
    
    # Clear input and rerun
    st.session_state.user_input = ""
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# JavaScript for auto-scroll and chat loading
st.markdown("""
<script>
    // Auto-scroll to bottom of chat
    function scrollToBottom() {
        const container = document.getElementById('chat-container');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    }
    
    // Scroll on page load and after messages
    setTimeout(scrollToBottom, 100);
    
    // Create global function for loading chats
    window.load_chat = function(chatId) {
        window.parent.streamlitApi.runMethod("load_chat", chatId);
    }
</script>
""", unsafe_allow_html=True)