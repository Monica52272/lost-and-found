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
@app.route('/post', methods=['GET', 'POST'])
def post_item():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        item_type = request.form['type']
        image = request.files['image']

        filename = image.filename
        image.save('static/uploads/' + filename)

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO items (title, description, type, image, status)
            VALUES (?, ?, ?, ?, ?)
        """, (title, description, item_type, filename, 'open'))
        conn.commit()
        conn.close()

        return "Item Posted Successfully"

    return render_template('post_item.html')
@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    items = c.fetchall()
    conn.close()

    return render_template('admin.html', items=items)
