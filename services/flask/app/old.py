from flask import Flask

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Import routes
from app import routes