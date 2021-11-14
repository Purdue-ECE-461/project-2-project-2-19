# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 01:22:59 2021

@author: garvi
"""

# File imports
from Project2 import app
from Project2 import util
from Project2 import macros

# Library imports
import os
from flask import render_template, flash, request
from google.cloud import storage


@app.route("/")
@app.route("/home")
def homepage():
    if (macros.first_load == True):
        flash('Welcome back!')
        macros.first_load = False
    return render_template("index.html", title="NPM-Registry Group 19")


@app.route("/docs")
def docs():
    return render_template("index.html", title="docs page")



@app.route("/upload", methods=['POST', 'GET'])
def upload():
    '''
    Code borrowed from google-docs.
        https://cloud.google.com/appengine/docs/flexible/python/using-cloud-storage
    '''
    if request.method == 'POST':

        # Verify the auth works.
        util.implicit()

        f = request.files['file']

        if not f:
            return 'No file uploaded.', 400

        gcs = storage.Client()
        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket(macros.CLOUD_STORAGE_BUCKET)

        # Create a new blob and upload the file's content.
        blob = bucket.blob(f.filename)

        blob.upload_from_string(
            f.read(),
            content_type=f.content_type
        )

        # Make the blob public. This is not necessary if the
        # entire bucket is public.
        # See https://cloud.google.com/storage/docs/access-control/making-data-public.
        blob.make_public()

        # The public URL can be used to directly access the uploaded file via HTTP.
        print(blob.public_url)

        flash("File added to the Cloud")

    return render_template("index.html", title="docs page")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
