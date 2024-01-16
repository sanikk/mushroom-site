from sqlalchemy.sql import text
from app import db


# Account
def get_user(username, password):
    sql = text("SELECT * FROM Account WHERE username = :username AND password = :password")
    return db.session.execute(sql, {"username": username, "password": password}).fetchone()


def add_user(username, password):
    sql = text("INSERT INTO account (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username": username, "password": password})
    db.session.commit()


# Mushroom
def add_mushroom(name, family_id, season_start, season_end):
    sql = text("INSERT INTO mushroom (name, family_id, season_start, season_end) VALUES (:name, :family_id, :season_start, :season_end)")
    db.session.execute(sql, {"name": name, "family_id": family_id, "season_start": season_start, "season_end": season_end})
    db.session.commit()


def get_mushrooms():
    return db.session.execute(
        text('SELECT M.name, F.name,M.season_start, M.season_end FROM mushroom M JOIN family F ON M.family_id = F.id')).fetchall()


# Family
def get_family_list():
    return db.session.execute(text('SELECT id, name FROM family')).fetchall()


# Sightings
def get_sightings():
    return db.session.execute(text('SELECT id, date, mushroom, location FROM sighting')).fetchall()
