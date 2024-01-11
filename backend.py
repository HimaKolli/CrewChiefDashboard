# backend.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, namespace='/chat')  # Specify the namespace

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("message", namespace='/chat')  # Specify the namespace for the event
def handle_message(data):
    emit("message", {"username": data["username"], "message": data["message"]}, namespace='/chat', broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)
