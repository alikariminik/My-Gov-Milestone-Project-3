import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Home
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


# Cabinet page
@app.route("/cabinet", methods=["GET", "POST"])
def cabinet():
    cabinet = list(mongo.db.cabinet.find())
    return render_template("cabinet.html", cabinet=cabinet)


# Sign Up page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("signup"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("signup.html")


# Log in page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# Profile page
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    return render_template("profile.html", username=username)


# Log out
@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Add Minister
@app.route("/add_minister", methods=["GET", "POST"])
def add_minister():
    if request.method == "POST":
        new_minister = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "gender": request.form.get("gender"),
            "dob": request.form.get("dob"),
            "role": request.form.get("role"),
            "constituency": request.form.get("constituency"),
            "profile_pic": request.form.get("profile_pic"),
        }
        mongo.db.cabinet.insert_one(new_minister)
        flash("Minister Successfully Added")

    return redirect(url_for("cabinet"))


# Edit Minister
@app.route("/edit_minister/<cab_id>", methods=["GET", "POST"])
def edit_minister(cab_id):
    if request.method == "POST":
        updated_details = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "gender": request.form.get("gender"),
            "dob": request.form.get("dob"),
            "role": request.form.get("role"),
            "constituency": request.form.get("constituency"),
            "profile_pic": request.form.get("profile_pic"),        
        }
        mongo.db.cabinet.update_one({"_id": ObjectId(cab_id)}, {"$set": updated_details})
        flash("Minister Details Updated")
        return redirect(url_for("cabinet"))
    
    cab = mongo.db.cabinet.find_one({"_id": ObjectId(cab_id)})
    return render_template("edit_minister.html", cab=cab)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
