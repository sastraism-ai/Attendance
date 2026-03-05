
from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "saradhi_secret"

def connect():
    return sqlite3.connect("saradhi.db")

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/auth", methods=["POST"])
def auth():
    email = request.form["email"]
    password = request.form["password"]

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE email=? AND password=?", (email, password))
    user = cur.fetchone()

    if user:
        session["user"] = user[1]
        session["id"] = user[0]
        session["role"] = user[4]

        if user[4] == "admin":
            return redirect("/admin")

        return redirect("/dashboard")

    return "Invalid login"

@app.route("/dashboard")
def dashboard():
    emp = session["id"]
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM attendance WHERE employee_id=?", (emp,))
    days = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM work_reports WHERE employee_id=?", (emp,))
    reports = cur.fetchone()[0]

    score = min(100, (days*5 + reports*10))

    cur.execute("SELECT date, check_in, check_out FROM attendance WHERE employee_id=?", (emp,))
    data = cur.fetchall()

    return render_template("dashboard.html", records=data, score=score)

@app.route("/checkin")
def checkin():
    emp = session["id"]
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M")

    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO attendance(employee_id,date,check_in) VALUES(?,?,?)", (emp,date,time))
    conn.commit()

    return redirect("/dashboard")

@app.route("/checkout")
def checkout():
    emp = session["id"]
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M")

    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE attendance SET check_out=? WHERE employee_id=? AND date=?", (time,emp,date))
    conn.commit()

    return redirect("/dashboard")

@app.route("/report", methods=["POST"])
def report():
    emp = session["id"]
    task = request.form["task"]
    date = datetime.now().strftime("%Y-%m-%d")

    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO work_reports(employee_id,date,task) VALUES(?,?,?)", (emp,date,task))
    conn.commit()

    return redirect("/dashboard")

@app.route("/admin")
def admin():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT e.name,a.date,a.check_in,a.check_out
    FROM attendance a
    JOIN employees e ON a.employee_id=e.id
    """)
    data = cur.fetchall()

    return render_template("admin.html", records=data)

@app.route("/analytics")
def analytics():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT date, COUNT(employee_id) FROM attendance GROUP BY date")
    data = cur.fetchall()

    dates = [d[0] for d in data]
    counts = [d[1] for d in data]

    return render_template("analytics.html", dates=dates, counts=counts)

@app.route("/chatbot", methods=["POST"])
def chatbot():
    msg = request.json["message"]

    reply = "SARADHI AI Assistant: This feature can be connected to OpenAI API for HR queries."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
