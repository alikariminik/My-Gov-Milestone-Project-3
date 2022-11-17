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


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
