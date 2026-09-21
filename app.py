from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# This is temporary memory storage.
# Emails disappear when we stop the application.
emails = []


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()

        if email and email not in emails:
            emails.append(email)

        return redirect(url_for("home"))

    return render_template("index.html", emails=emails)


if __name__ == "__main__":
    app.run(debug=True)