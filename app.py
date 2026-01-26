from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "lostandfound"

# ---------- LOGIN ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # DEMO LOGIN (Render-safe)
        if email == "admin@gmail.com" and password == "admin123":
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid login details")

    return render_template("login.html")


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    return """
    <h1>Lost and Found Management</h1>
    <p>Login Successful</p>
    """


if __name__ == "__main__":
    app.run()
