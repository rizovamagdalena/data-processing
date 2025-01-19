#app.py

from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from src.backend.app.routes import stock_routes

app = Flask(__name__)
CORS(app)

scheduler = BackgroundScheduler(daemon=True)

# Register Blueprints
app.register_blueprint(stock_routes)
