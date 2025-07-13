from flask import Flask

app = Flask(__name__)

# Deplegar las rutas desde __init__.py
from ibero import routes
