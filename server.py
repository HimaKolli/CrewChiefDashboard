# from flask import Flask, render_template
# from flask_socketio import SocketIO, emit

# app = Flask(__name__)
# socketio = SocketIO(app)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @socketio.on('message')
# def handle_message(data):
#     emit('message', data, broadcast=True)
    
# if __name__ == '__main__':
#     socketio.run(app, debug=True)
# backend.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("message")
def handle_message(data):
    emit("message", {"username": data["username"], "message": data["message"]}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
