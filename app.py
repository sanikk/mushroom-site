from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import calendar
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///" + os.getenv("DBNAME")
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    family_id = request.form["family"]
    season_start = request.form["season_start"]
    season_end = request.form["season_end"]
    sql = text("INSERT INTO mushroom (name, family_id, season_start, season_end) VALUES (:name, :family_id, :season_start, :season_end)")
    db.session.execute(sql, {"name": name, "family_id": family_id, "season_start": season_start, "season_end": season_end})
    db.session.commit()
    return redirect("/mushrooms")


@app.route("/sightings")
def sightings():
    find_result = db.session.execute(text('SELECT id, date, mushroom, location FROM sighting'))


@app.route("/mushroom_form")
def add_mushroom():
    family_result = db.session.execute(text('SELECT id, name FROM family'))
    families = family_result.fetchall()
    months = [(i, calendar.month_name[i]) for i in range(1, 13)]
    return render_template("add_mushroom.html", families=families, months=months)
    # return redirect("/mushrooms")


@app.route("/mushrooms")
def mushrooms_page():
    mushrooms_result = db.session.execute(text('SELECT M.name, F.name,M.season_start, M.season_end FROM mushroom M JOIN family F ON M.family_id = F.id'))
    mushrooms = mushrooms_result.fetchall()
    return render_template("mushrooms.html", mushrooms=mushrooms)


@app.route("/forum")
def forum():
    return render_template("forum.html")


@app.route("/documents")
def documents():
    return render_template("documents.html")


@app.route("/families")
def families():
    family_result = db.session.execute(text('SELECT * FROM family'))
    families = family_result.fetchall()
    return render_template("families.html", families=families)


@app.route("/seasons")
def seasons():
    return render_template("seasons.html")
