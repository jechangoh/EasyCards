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

    conn2 = sqlite3.connect("flashcards.db")

    with open("schema.sql") as f:
        conn2.executescript(f.read())

    cur = conn2.cursor()

    count = cur.execute("SELECT COUNT(*) FROM cards")

    if count != 0:
        cards = conn.execute("SELECT * FROM cards").fetchall()
        conn.close()
        return render_template("index.html", cards=cards)
    
    return render_template("index.html")
    

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


@app.route("/remove", methods=["POST"])
def remove():
    conn = sqlite3.connect("flashcards.db")

    with open("schema.sql") as f:
        conn.executescript(f.read())

    cur = conn.cursor()

    card = request.form.get("id")
    if card:
        cur.execute("DELETE FROM cards WHERE id = ?", card)
        conn.commit()
        conn.close()
    
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    conn = sqlite3.connect("flashcards.db")

    with open("schema.sql") as f:
        conn.executescript(f.read())

    cur = conn.cursor()

    count = cur.execute("SELECT COUNT(*) FROM cards")

    if count != 0:
        cur.execute("DELETE FROM cards")
        conn.commit()
        conn.close()

    return redirect("/")
    
