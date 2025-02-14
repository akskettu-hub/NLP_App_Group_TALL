from flask import Flask
from config import Config 

app = Flask(__name__)
app.config.from_object(Config)
# Enable debug mode (flask automatically reloads when changes occur)
app.config['DEBUG'] = True

from app import routes