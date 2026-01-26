from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "lostandfound"

DB_NAME = "database.db"

# ---------- DATABASE INIT ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    # default user insert (only once)
    cur.execute("SELECT * FROM users WHERE email=?", ("admin@gmail.com",))
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            ("admin@gmail.com", "admin123")
        )

    conn.commit()
    conn.close()

init_db()

# ---------- ROUTES ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid login details")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return "<h1>Lost and Found Management - Dashboard</h1>"


if __name__ == "__main__":
    app.run(debug=True)
