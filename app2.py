import streamlit as st
import socketio

# Initialize Streamlit
st.title("Streamlit Live Chat App")

# Create a Streamlit sidebar for username input
username = st.sidebar.text_input("Enter your username", "User")

# Create a Streamlit text area for the chat messages
chat_messages = st.text_area("Chat", "", height=400, max_chars=500, key="chat")

# Create a SocketIO client
sio = socketio.Client()

# SocketIO event for handling incoming messages
@sio.on("message")
def handle_message(data):
    st.text(f"{data['username']}: {data['message']}")

# Streamlit button to send messages
if st.button("Send Message"):
    message_input = st.text_input("Enter your message", "")
    
    # Emit a SocketIO event to send the message to the server
    sio.emit("message", {"username": username, "message": message_input})

# Connect to the SocketIO server
sio.connect("http://localhost:8501")

# Streamlit event loop
st.experimental_rerun()