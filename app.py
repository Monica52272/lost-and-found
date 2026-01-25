from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__, static_folder="static")
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()

        if user:
            session["user"] = username
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO users(username,password) VALUES (?,?)", (username, password))
        db.commit()
        return redirect("/")
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")

@app.route("/lost", methods=["GET", "POST"])
def lost():
    if "user" not in session:
        return redirect("/")
    if request.method == "POST":
        data = (
            "Lost",
            request.form["name"],
            request.form["description"],
            request.form["location"],
            request.form["date"]
        )
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO items(type,name,description,location,date) VALUES (?,?,?,?,?)", data)
        db.commit()
    return render_template("lost.html")

@app.route("/found", methods=["GET", "POST"])
def found():
    if "user" not in session:
        return redirect("/")
    if request.method == "POST":
        data = (
            "Found",
            request.form["name"],
            request.form["description"],
            request.form["location"],
            request.form["date"]
        )
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO items(type,name,description,location,date) VALUES (?,?,?,?,?)", data)
        db.commit()
    return render_template("found.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "Lost and Found Working!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

