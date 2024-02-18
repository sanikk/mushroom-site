from flask import redirect, render_template, request, session
import calendar
from app import app
from db_operations import (get_mushrooms, get_sightings, get_family_list, create_user, create_mushroom,
                           check_user, get_user_list, get_new_sightings, create_sighting, create_family,
                           get_account_info)


@app.route("/")
def index():
    return render_template("index.html")


# User stuff
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    ret = check_user(username, password)
    if ret:
        session["username"] = ret
        return redirect("/")
    # TODO
    # throw error, ask again
    raise ValueError("username or password")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/accounts/add", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    if " " not in username:
        ret = create_user(username, password)
        if ret:
            session["username"] = ret
            return redirect("/")
    # TODO
    # throw error, ask again
    raise ValueError("username or password")


@app.route("/accounts")
# TODO
# AUTH to admin
def accounts():
    return render_template("accounts.html", users=get_user_list())


@app.route("/accounts/<int:id>")
def account_page(id_to_look_for):
    # TODO
    account_info = get_account_info(id_to_look_for)
    return render_template("todo.html", account_info=account_info)
    pass


# Mushrooms

@app.route("/mushrooms")
def mushrooms_page():
    return render_template("mushrooms.html", mushrooms=get_mushrooms())


@app.route("/mushrooms/add", methods=["POST"])
def add_mushroom():
    create_mushroom(
        request.form["name"], request.form["family"], request.form["season_start"], request.form["season_end"])
    return redirect("/mushrooms")


@app.route("/mushrooms/<mushroom_id:int>")
# TODO
def mushroom_page(mushroom_id):
    return render_template("todo.html")


@app.route("/mushrooms/new")
def new_mushroom_page():
    months = [(i, calendar.month_name[i]) for i in range(1, 13)]
    return render_template("add_mushroom.html", families=get_family_list(), months=months)


# Sightings

@app.route("/sightings")
def sightings():
    return render_template("sightings.html", sightings=get_new_sightings())


@app.route("/sightings/<sighting_id:int>")
# TODO
def sighting_page(sighting_id):
    return render_template("todo.html")


@app.route("/sightings/new")
def new_sighting_page():
    pass


@app.route("/sightings/add", methods=["POST"])
def add_sighting():
    create_sighting(
        request.form["mushroom"], request.form["family"], request.form["harvest_date"], request.form["rating"])
    return redirect("/mushrooms")


@app.route("/statistics")
def statistics():
    return render_template("statistics.html")


@app.route("/families")
def families():
    return render_template("families.html", families=get_family_list())


@app.route("/families/<family_id:int>")
def family_page(family_id):
    # TODO
    return render_template("todo.html")


@app.route("/families/add", methods=["POST"])
def add_family():
    create_family(
        request.form["mushroom"], request.form["family"], request.form["harvest_date"], request.form["rating"])
    return redirect("/families")


@app.route("/families/new")
def new_family_page():
    return render_template("add_family.html")


@app.route("/seasons")
def seasons():
    return render_template("seasons.html")
