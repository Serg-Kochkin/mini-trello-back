from flask import Flask
from app.database import initialize_tables
from flask_cors import CORS

flask_app = Flask(__name__)
CORS(flask_app)
initialize_tables()
