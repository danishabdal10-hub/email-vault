import os
from datetime import datetime, timezone

from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

app = Flask(__name__)

# Connect to MongoDB running in our Docker container.
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
database = client["email_vault"]
emails_collection = database["emails"]

# Prevent the same email being saved twice.
emails_collection.create_index("email", unique=True)

@app.route("/health")
def health():
    try:
        client.admin.command("ping")
        
        return {
            "status": "healthy",
            "database": "connected"
        }, 200

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }, 503


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()

        if not email:
            message = "Please enter an email."
        else:
            try:
                emails_collection.insert_one(
                    {
                        "email": email,
                        "created_at": datetime.now(timezone.utc)
                    }
                )
                return redirect(url_for("home"))
            except DuplicateKeyError:
                message = "This email was already added."

    saved_emails = list(
        emails_collection.find().sort("created_at", -1)
    )

    return render_template(
        "index.html",
        emails=saved_emails,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)