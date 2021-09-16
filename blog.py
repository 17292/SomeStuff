
# Imports flask
from flask import Flask,g, render_template, request, redirect, session, url_for, g, abort, flash  
import sqlite3
import os.path
from flask.helpers import flash


# Global variable
class User:
    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User: {self.username}>"

# List of users
users = []
users.append(User(id=0, username= "Micah", password= "1234"))

print(users)

app = Flask(__name__)
app.secret_key = "secret"


# Checks sessions and places it in g object 
@app.before_request
def before_request():
    g.user = None
    if "user_id" in session:
        # Finds user's id
        for user in users:
            if user.id == session["user_id"]:
                g.user = user

# Makes a connection with database
DATABASE = "blog.db"

# Login system 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.pop("user_id", None)
        username = request.form["username"]
        password = request.form["password"]
        # Allows the user to register 
        if request.form.get("register"):
            user = User(len(users), username, password)
            users.append(user)
            session["user_id"] = user.id
            return redirect(url_for("profile"))
        for user in users:
            # If users can't supply the correct username and password a warning sign pops up
            if user.username == username and user.password == password:
                session["user_id"] = user.id
                return redirect(url_for("home"))
            flash("Failed to login")
            return redirect(url_for("login"))  
    return render_template("login.html")

# Users that has logged in have a button that'll log them out
@app.route ("/logout")
def logout():
    session.pop ("user_id", None)
    return redirect(url_for("login"))  
    
# A page of the user's profile
@app.route("/profile")
def profile():
    # Users can't access their profile unless they login first
    if not g.user:
        return redirect(url_for("login"))

    return render_template("profile.html")

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
        sql = "INSERT INTO article(heading,body) VALUES (?,?)"
        cursor.execute(sql, (new_heading, new_body))
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