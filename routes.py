from flask import redirect, render_template, request
import calendar
from app import app
from db_operations import add_mushroom, get_sightings, get_family_list, get_mushrooms


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
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


@app.route("/documents")
def documents():
    return render_template("documents.html")


@app.route("/families")
def families():
    return render_template("families.html", families=get_family_list())


@app.route("/seasons")
def seasons():
    return render_template("seasons.html")
