from flask import Flask
import connexion
from project_2 import routes

# app = Flask(__name__)
app = connexion.App(__name__, specification_dir='./')
