# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 01:22:59 2021

@author: garvi
"""

from Project2 import app
from flask import render_template

@app.route("/")
def homepage():
    return render_template("index.html", title="HOME PAGE")

@app.route("/docs")
def docs():
    return render_template("index.html", title="docs page")

@app.route("/about")
def about():
    return render_template("index.html", title="about page")

if __name__ == "__main__":
    app.run(debug=True)
