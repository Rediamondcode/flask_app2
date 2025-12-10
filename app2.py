from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"   # Required for session management

# Dummy user (NO DATABASE)
USER = {
    "username": "admin",
    "password": "12345"
}

MESSAGES = []  # Stores contact form submissions in memory

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USER["username"] and password == USER["password"]:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid login credentials", "danger")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", messages=MESSAGES)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")

        MESSAGES.append({"name": name, "message": message})
        flash("Message submitted successfully!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
