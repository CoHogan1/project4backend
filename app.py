from flask import Flask, jsonify
from resources.users import users
import models
from flask_cors import CORS
from flask_login import LoginManager
import os
from dotenv import load_dotenv
#socketIO -----------
from flask import Flask, render_template
from flask_socketio import SocketIO, send


load_dotenv()

DEBUG=True
PORT=8000

app = Flask(__name__) # instantiating the Flask class to create an app
app.secret_key = os.environ.get("FLASK_APP_SECRET")
app.config['SECRET_KEY'] = 'socket'
#print(os.environ.get("FLASK_APP_SECRET"))


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return models.User.get(models.User.id == user_id)

CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(users, url_prefix='/api/v1/users')

#socketIO
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")# timing of this may be important.

@app.route('/')
def hello():
    return 'server is running'

#socketIO
@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)
    # default returns the message to the sender
    send(data, broadcast=True) # sends message to all.
    return None


if __name__ == '__main__':
    models.init()
    app.run(debug=DEBUG, port=PORT)
    socketio.run(app)
