# Imports flask
from flask import Flask,g, render_template, request, redirect, session, url_for, g, abort, flash  
import sqlite3
import os.path
from flask.helpers import flash
from werkzeug.security import check_password_hash, generate_password_hash


# Global variable
class User:
    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User: {self.username}>"

app = Flask(__name__)
app.secret_key = "secret"


# Checks sessions and places it in g object 
@app.before_request
def before_request():
    g.user = None
    if "user_id" in session:
        # Finds user's id
        sql = "SELECT id, name, password FROM user WHERE id = ?"
        cursor = get_db().cursor()
        cursor.execute(sql, (session["user_id"], ))
        user = cursor.fetchone()
        if user:
            g.user = User(*user)

# Makes a connection with database
DATABASE = "blog.db"

# Login system 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.pop("user_id", None)
        username = request.form["username"]
        password = request.form["password"]
        connection = get_db()
        cursor = connection.cursor()
        redirect_to = url_for("home")
        # Allows the user to register 
        if request.form.get("register"):
            sql = "INSERT INTO user(name, password) VALUES (?, ?)"
            cursor.execute(sql, (
                username, 
                generate_password_hash(password)
                )
            )
            connection.commit()
            redirect_to = url_for("profile")
        sql = "SELECT id, name, password FROM user WHERE name = ?"
        cursor.execute(sql, (username, ))
        user = cursor.fetchone()
        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            return redirect(redirect_to)
        flash("Failed to login")
        return redirect(url_for("login"))
    return render_template("login.html")

# Users that has logged in have a button that'll log them out
@app.route ("/logout")
def logout():
    if "user_id" in session:
        flash("logged out successfully")
        session.pop ("user_id", None)
        g.user = None
    return redirect(url_for("login"))  
    
# A page of the user's profile
@app.route("/profile")
def profile():
    # Users can't access their profile unless they login first
    if not g.user:
        return redirect(url_for("login"))
    cursor = get_db().cursor()
    return render_template("profile.html",)

# Connects to the database
def get_db():
    db= getattr(g, "_datebase", None)
    if db is None:
        db = g._datebase = sqlite3.connect(DATABASE)
    return db
 
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_datebase", None)
    if db is not None:
        db.close()

# Route to home.html
@app.route("/")
def home():
    return render_template("home.html")

# Gets articles from the database
@app.route("/article")
def article():
    cursor = get_db().cursor()
    sql = "SELECT * FROM article"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("article.html", results=results)
    
# A route to the contant page
@app.route("/contact")
def contact():
    return render_template("contact.html") 

# Adds articles to article.html 
@app.route("/add", methods= ["GET","POST"])
def add():
    # User has to login to add articles
    if not g.user:
        return redirect(url_for("login"))
    # Once logged in user can upload their post
    # They can upload as many headings and articles as they want 
    if request.method == "POST":
        cursor = get_db().cursor()
        new_heading = request.form["article_heading"]
        if len(new_heading) > 20:
            return redirect("/add")
        new_body = request.form["article_body"]
        if len(new_body) > 500:
            return redirect("/add")
        sql = "INSERT INTO article(heading,body, user_id) VALUES (?,?,?)"
        cursor.execute(sql, (new_heading, new_body, g.user.id))
        get_db().commit()
    return redirect('/')

# Deletes articles that have been posted
@app.route('/delete', methods= ["GET","POST"])
def delete():
    # User has to login before able to delete
    if not g.user:
        return redirect(url_for("login"))
    # Once logged in user can delete posts   
    # They can delete as many headings and articles as they want   
    if request.method == "POST":
        cursor = get_db().cursor()
        id = int(request.form["article_heading"])
        sql = "DELETE FROM article WHERE id=?"
        cursor.execute(sql,(id,))
        get_db().commit()
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)