from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect("users.db")

def init_db():
    con = get_db()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lost_items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS found_items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT
        )
    """)
    con.commit()
    con.close()

init_db()

# ---------- LOGIN ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print(request.form)
        username = request.form['username']
        password = request.form['password']

        con = get_db()
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cur.fetchone()
        con.close()

        if user:
            session["user"] = user[1]
            session["role"] = user[3]
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Login Details"

    return render_template("login.html")

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

# ---------- ADD LOST ----------
@app.route("/lost", methods=["GET", "POST"])
def lost():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["description"]

        con = get_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO lost_items(title, description) VALUES (?,?)",
            (title, desc)
        )
        con.commit()
        con.close()
        return redirect(url_for("dashboard"))

    return render_template("add_lost.html")

# ---------- ADD FOUND ----------
@app.route("/found", methods=["GET", "POST"])
def found():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["description"]

        con = get_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO found_items(title, description) VALUES (?,?)",
            (title, desc)
        )
        con.commit()
        con.close()
        return redirect(url_for("dashboard"))

    return render_template("add_found.html")

# ---------- ADMIN ----------
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return "Access Denied"

    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM lost_items")
    lost = cur.fetchall()
    cur.execute("SELECT * FROM found_items")
    found = cur.fetchall()
    con.close()

    return render_template("admin.html", lost=lost, found=found)

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/view-lost")
def view_lost():
    if "user" not in session:
        return redirect("/")
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM items WHERE type='Lost'")
    data = cur.fetchall()
    return render_template("view.html", items=data, title="Lost Items")

@app.route("/view-found")
def view_found():
    if "user" not in session:
        return redirect("/")
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM items WHERE type='Found'")
    data = cur.fetchall()
    return render_template("view.html", items=data, title="Found Items")

