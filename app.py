import streamlit as st
import random
from api_client import APIClient


def generate_thread_id() -> str:
    """Generate a random 5-digit thread ID."""
    return str(random.randint(10000, 99999))


def initialize_session_state():
    """Initialize all session state variables."""
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False
    if "current_thread_id" not in st.session_state:
        st.session_state.current_thread_id = None
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}  # {thread_id: [messages]}
    if "session_labels" not in st.session_state:
        st.session_state.session_labels = {}  # {thread_id: label}


def handle_login(username: str, password: str):
    """Handle user login."""
    if not username or not password:
        st.sidebar.error("Please enter both username and password")
        return
    
    with st.spinner("Logging in..."):
        response, error = APIClient.login(username, password)
    
    if response and "access_token" in response:
        st.session_state.access_token = response["access_token"]
        st.session_state.is_authenticated = True
        st.sidebar.success("Login successful!")
        st.rerun()
    else:
        error_msg = error or "Login failed. Please check your credentials."
        st.sidebar.error(error_msg)


def handle_logout():
    """Handle user logout."""
    st.session_state.access_token = None
    st.session_state.is_authenticated = False
    st.session_state.current_thread_id = None
    st.session_state.chat_sessions = {}
    st.session_state.session_labels = {}
    st.rerun()


def create_new_chat():
    """Create a new chat session."""
    thread_id = generate_thread_id()
    st.session_state.current_thread_id = thread_id
    st.session_state.chat_sessions[thread_id] = []
    # Generate a label for the session (first few words of first message or default)
    st.session_state.session_labels[thread_id] = f"Chat {thread_id}"
    st.rerun()


def switch_to_thread(thread_id: str):
    """Switch to a different chat thread."""
    st.session_state.current_thread_id = thread_id
    st.rerun()


def get_session_label(thread_id: str) -> str:
    """Get the label for a chat session."""
    if thread_id in st.session_state.session_labels:
        return st.session_state.session_labels[thread_id]
    return f"Chat {thread_id}"


def update_session_label(thread_id: str, first_message: str):
    """Update session label based on first message."""
    if thread_id not in st.session_state.session_labels or \
       st.session_state.session_labels[thread_id].startswith("Chat "):
        # Create a label from first message (first 30 chars)
        label = first_message[:30].strip()
        if len(first_message) > 30:
            label += "..."
        st.session_state.session_labels[thread_id] = label or f"Chat {thread_id}"


# Initialize session state
initialize_session_state()

# Sidebar
with st.sidebar:
    st.title("OCAP Chat")
    
    # Login Section
    if not st.session_state.is_authenticated:
        st.header("Login")
        username = st.text_input("Username", key="login_username", placeholder="user@example.com")
        password = st.text_input("Password", type="password", key="login_password", placeholder="Enter password")
        
        if st.button("Login", type="primary", use_container_width=True):
            handle_login(username, password)
    else:
        st.success("✓ Logged in")
        if st.button("Logout", use_container_width=True):
            handle_logout()
        
        st.divider()
        
        # Chat History Section
        st.header("Chat History")
        
        # Display existing chat sessions
        if st.session_state.chat_sessions:
            for thread_id in sorted(st.session_state.chat_sessions.keys(), reverse=True):
                label = get_session_label(thread_id)
                is_active = st.session_state.current_thread_id == thread_id
                
                # Style active session differently
                button_label = f"● {label}" if is_active else label
                if st.button(
                    button_label,
                    key=f"thread_{thread_id}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary"
                ):
                    switch_to_thread(thread_id)
        
        # New Chat Button
        st.divider()
        if st.button("➕ New Chat", type="primary", use_container_width=True):
            create_new_chat()

# Main Chat Interface
if not st.session_state.is_authenticated:
    st.title("Welcome to OCAP Chat")
    st.info("Please login using the sidebar to start chatting.")
else:
    st.title("OCAP Assistant")
    
    # Initialize current thread if none exists
    if st.session_state.current_thread_id is None:
        create_new_chat()
    
    current_thread = st.session_state.current_thread_id
    
    # Display chat messages from current thread
    if current_thread in st.session_state.chat_sessions:
        messages = st.session_state.chat_sessions[current_thread]
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        if current_thread not in st.session_state.chat_sessions:
            st.session_state.chat_sessions[current_thread] = []
        
        st.session_state.chat_sessions[current_thread].append({"role": "user", "content": prompt})
        
        # Update session label if this is the first message
        if len(st.session_state.chat_sessions[current_thread]) == 1:
            update_session_label(current_thread, prompt)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process query with API
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_data, error = APIClient.process_query(
                    prompt,
                    current_thread,
                    st.session_state.access_token
                )
            
            if response_data:
                # Extract response text from API response
                # Adjust this based on your actual API response structure
                if isinstance(response_data, dict):
                    # Try common response fields
                    response_text = response_data.get("response") or \
                                   response_data.get("answer") or \
                                   response_data.get("message") or \
                                   str(response_data)
                else:
                    response_text = str(response_data)
                
                st.markdown(response_text)
                st.session_state.chat_sessions[current_thread].append({
                    "role": "assistant",
                    "content": response_text
                })
            else:
                error_msg = error or "Failed to process query. Please try again."
                st.error(error_msg)
                st.session_state.chat_sessions[current_thread].append({
                    "role": "assistant",
                    "content": f"Error: {error_msg}"
                })
