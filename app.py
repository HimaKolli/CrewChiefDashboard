# app.py
import streamlit as st
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from socketIO_client import SocketIO

def main():
    st.title("Live Chat App")

    # Get user input (username and message)
    username = st.text_input("Enter your username:")
    message = st.text_area("Type your message:")

    # Display the chat
    st.subheader("Chat:")
    chat_div = st.empty()  # Placeholder for the chat messages

    # Connect to the Flask-SocketIO server
    socketio = SocketIO('http://localhost', 5000)

    # Emit message to the server when the user sends a message
    if st.button("Send"):
        socketio.emit('message', {'username': username, 'message': message})

    # Handle incoming messages from the server
    @socketio.on('message')
    def handle_message(data):
        st.write(f"{data['username']}: {data['message']}")

if __name__ == "__main__":
    main()
