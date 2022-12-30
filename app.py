from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def db_connection():
    conn = sqlite3.connect('flashcards.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = db_connection()
    cards = conn.execute("SELECT * FROM cards").fetchall()
    conn.close()
    return render_template("index.html", cards=cards)


@app.route('/flashcards', methods=["POST"])
def flashcards():
    word = request.form.get("word")
    description = request.form.get("description")
    if not word or not description:
        return render_template("error.html")

    conn = sqlite3.connect("flashcards.db")

    with open("schema.sql") as f:
        conn.executescript(f.read())

    cur = conn.cursor()

    cur.execute("INSERT INTO cards (word, description) VALUES(?, ?)", (word, description))

    conn.commit()
    conn.close()
    
    return redirect("/")
