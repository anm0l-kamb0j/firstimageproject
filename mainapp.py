import os
from flask import Flask, render_template, request, redirect, url_for
from google.cloud import storage

# Set the path to the service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/project-1-449402-36d72f873921.json"

app = Flask(__name__)

# Google Cloud Storage configuration
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "cloudnativeproject1")
client = storage.Client()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Handle file upload
        file = request.files["image"]
        if file:
            # Generate a unique filename
            filename = file.filename
            # Upload the file to Google Cloud Storage
            bucket = client.bucket(BUCKET_NAME)
            blob = bucket.blob(filename)
            blob.upload_from_file(file)
            return redirect(url_for("home"))

    # List existing files in the bucket
    bucket = client.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs()
    images = [blob.name for blob in blobs]

    return render_template("homepage.html", images=images, BUCKET_NAME=BUCKET_NAME)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)