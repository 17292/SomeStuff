from flask import Flask,g, render_template, request, redirect  
import sqlite3

app = Flask(__name__)

DATEBASE = "blog.db"

def get_db():
    db= getattr(g, "_datebase", None)
    if db is None:
        db = g._datebase = sqlite3.connect(DATEBASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_datebase", None)
    if db is not None:
        db.close()

@app.route("/")
def home():
    cursor = get_db().cursor()
    sql = "SELECT * FROM article"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("home.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)