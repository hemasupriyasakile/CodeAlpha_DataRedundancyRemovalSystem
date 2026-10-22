from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("records.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()

create_table()


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Redundancy Removal System</title>
<style>
  
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 40px 16px;
    font-family: Arial, sans-serif;
    background: #eef2ff;
    color: #1e293b;
}

.container {
    max-width: 700px;
    margin: auto;
}

.header {
    background: #312e81;
    color: white;
    padding: 30px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 24px;
}

.header h1 {
    margin: 0 0 10px;
    font-size: 27px;
}

.header p {
    margin: 0;
    color: #e0e7ff;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 14px;
    margin-bottom: 22px;
    box-shadow: 0 5px 18px #1e293b12;
}

form label {
    display: block;
    margin: 15px 0 8px;
    font-weight: bold;
}

form input {
    display: block;
    width: 100%;
    margin-bottom: 16px;
    padding: 12px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-size: 15px;
}

form input:focus {
    outline: 2px solid #818cf8;
    border-color: #6366f1;
}

form button {
    display: block;
    width: 100%;
    margin-top: 20px;
    padding: 13px;
    background: #4f46e5;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
}

form button:hover {
    background: #3730a3;
}
.delete-btn {
    background: #dc2626;
    margin-top: 10px;
}

.delete-btn:hover {
    background: #991b1b;
}
.message {
    padding: 12px;
    background: #f1f5f9;
    border-radius: 8px;
    margin-top: 15px;
    overflow-wrap: anywhere;
}

.record {
    padding: 14px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    margin-top: 10px;
    overflow-wrap: anywhere;
}

.empty {
    color: #64748b;
}

footer {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    padding: 10px;
}
</style>
</head>

<body>
    <div class="container">

        <div class="header">
            <h1>Data Redundancy Removal System</h1>
            <p>Validate records. Prevent duplicates. Maintain accuracy.</p>
        </div>

        <div class="card">
            <h2>Add New Record</h2>

            <form method="POST">
                <label for="name">Full Name</label>
                <input id="name" name="name"
                       placeholder="Enter full name"
                       maxlength="100" required>

                <label for="email">Email Address</label>
                <input id="email" name="email"
                       type="email"
                       placeholder="Enter email address"
                       maxlength="254" required>

                <button type="submit">Add Record</button>
            </form>

            {% if message %}
                <div class="message">{{ message }}</div>
            {% endif %}
        </div>

        <div class="card">
            <h2>Saved Records ({{ records|length }})</h2>

            {% if records %}
               
{% for record in records %}
    <div class="record">
        <strong>{{ record[1] }}</strong><br>
        <span>{{ record[2] }}</span>

        <form method="POST"
              action="{{ url_for('delete_record', record_id=record[0]) }}"
              onsubmit="return confirm('Are you sure you want to delete this record?');">
            <button type="submit" class="delete-btn">
                Delete Record
            </button>
        </form>
    </div>
{% endfor %}

            {% else %}
                <p class="empty">No records added yet.</p>
            {% endif %}
        </div>

        <footer>
            Cloud Computing Project | Data Redundancy Removal System
        </footer>

    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()

        conn = sqlite3.connect("records.db")

        try:
            conn.execute(
                "INSERT INTO records (name, email) VALUES (?, ?)",
                (name, email)
            )
            conn.commit()
            message = "Record added successfully!"

        except sqlite3.IntegrityError:
            message = "Duplicate email! Record already exists."

        finally:
            conn.close()

        return redirect(url_for("home", message=message))

    message = request.args.get("message", "")

    conn = sqlite3.connect("records.db")
    records = conn.execute(
        "SELECT * FROM records ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template_string(
        HTML, records=records, message=message
    )
@app.route("/delete/<int:record_id>", methods=["POST"])
def delete_record(record_id):
    conn = sqlite3.connect("records.db")

    conn.execute(
        "DELETE FROM records WHERE id = ?",
        (record_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("home", message="Record deleted successfully!"))

if __name__ == "__main__":
    app.run(debug=True)

