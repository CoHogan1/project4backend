from flask import Flask, jsonify
from resources.dogs import dogs 
from resources.users import users
import models
from flask_cors import CORS
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG=True
PORT=8000

app = Flask(__name__) # instantiating the Flask class to create an app
app.secret_key = os.environ.get("FLASK_APP_SECRET")
print(os.environ.get("FLASK_APP_SECRET"))

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return models.User.get(models.User.id == user_id)

CORS(users, origins=['http://localhost:8000'], supports_credentials=True)
app.register_blueprint(users, url_prefix='/api/v1/users')

@app.route('/')
def hello():
    return 'server is running'

if __name__ == '__main__':
    models.initialize() # remember in express we required the db before we did app.listen
    app.run(debug=DEBUG, port=PORT)
