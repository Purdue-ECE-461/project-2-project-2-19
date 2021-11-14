from flask import Flask
import connexion


#app = Flask(__name__)
app = connexion.App(__name__, specification_dir='./')

from Project2 import routes
