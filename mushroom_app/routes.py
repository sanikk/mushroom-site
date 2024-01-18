from flask import redirect, render_template, request, session
import calendar
from app import app
from db_operations import add_mushroom, get_sightings, get_family_list, get_mushrooms, get_user, add_user


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # CHECK GOES HERE
    rep = get_user(username, password)
    if rep:
        session["username"] = rep[1]
        # return render_template("sightings.html", sightings=rep)
    return redirect("/")
    # return render_template("sightings.html", sightings=rep)
    # muuten ilmoitetaan virheestä ja jatketaan kysymymistä


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    rep = get_user(username, password)
    if not rep:
        add_user(username, password)
        rep = get_user(username, password)
        session["username"] = rep[1]
        return redirect("/")
    # muuten ilmotetaan virheestä ja jatketaan kysymistä


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/add_mushroom", methods=["POST"])
def add():
    add_mushroom(
        request.form["name"], request.form["family"], request.form["season_start"], request.form["season_end"])
    return redirect("/mushrooms")


@app.route("/sightings")
def sightings():
    return render_template("sightings.html", sightings=get_sightings())


@app.route("/mushroom_form")
def add_mushroom():
    months = [(i, calendar.month_name[i]) for i in range(1, 13)]
    return render_template("add_mushroom.html", families=get_family_list(), months=months)


@app.route("/mushrooms")
def mushrooms_page():
    return render_template("mushrooms.html", mushrooms=get_mushrooms())


@app.route("/forum")
def forum():
    return render_template("forum.html")


@app.route("/statistics")
def statistics():
    return render_template("statistics.html")


@app.route("/families")
def families():
    return render_template("families.html", families=get_family_list())


@app.route("/seasons")
def seasons():
    return render_template("seasons.html")
