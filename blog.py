from flask import Flask,g, render_template, request, redirect, session, url_for, g, abort, flash  
import sqlite3
from flask.helpers import flash

class User:
    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User:{self.username}"

users = []
users.append(User(id=1, username= "Micah", password= "1234"))

print(users)

app = Flask(__name__)
app.secret_key = "secret"

@app.before_request
def before_request():
    g.user = None
    if "user_id" in session:
        user = [x for x in users if x.id == session["user_id"]][0]
        g.user = user

DATEBASE = "blog.db"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.pop("user_id", None)
        username = request.form["username"]
        password = request.form["password"]
        for user in users:
            if user.username == username and user.password == password:
                session["user_id"] = user.id
                return redirect(url_for("home"))
            flash("Failed to login")
            return redirect(url_for("login"))  
    return render_template("login.html")

@app.route ("/logout")
def logout():
    session.pop ("user_id", None)
    return redirect(url_for("login"))  

@app.route("/profile")
def profile():
    if not g.user:
        return redirect(url_for("login"))

    return render_template("profile.html")

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
    return render_template("home.html")

@app.route("/article")
def article():
    cursor = get_db().cursor()
    sql = "SELECT * FROM article"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("article.html", results=results)
    

@app.route("/contact")
def contact():
    return render_template("contact.html") 

@app.route("/add", methods= ["GET","POST"])
def add():
    if request.method == "POST":
        cursor = get_db().cursor()
        new_heading = request.form["article_heading"]
        new_body = request.form["article_body"]
        sql = "INSERT INTO article(heading,body) VALUES (?,?)"
        cursor.execute(sql, (new_heading, new_body))
        get_db().commit()
    return redirect('/')

@app.route('/delete', methods= ["GET","POST"])
def delete():
    if request.method == "POST":
        cursor = get_db().cursor()
        id = int(request.form["article_heading"])
        sql = "DELETE FROM article WHERE id=?"
        cursor.execute(sql,(id,))
        get_db().commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)