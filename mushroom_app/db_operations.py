from sqlalchemy.sql import text
from app import db
from werkzeug.security import check_password_hash, generate_password_hash


# Account
def __get_user(username: str):
    """
    Get userrow by username

    :param username: string
    :return:
        userrow or None
    """
    sql = text("SELECT * FROM Account WHERE username = :username")
    return db.session.execute(sql, {"username": username}).fetchone()


def check_user(username: str, password: str) -> str:
    """
    Check password against password hash

    :param username:
    :param password:
    :return:
        username or ""
    """
    ret = __get_user(username)
    if check_password_hash(ret, password):
        return ret[1]
    return ""


def create_user(username: str, password: str) -> str:
    """
    Add username and password hash to db.

    :param username:
    :param password:
    :return:
        username or ""
    """
    if __get_user(username):
        return ""
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO account (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username": username, "password": hash_value})
    db.session.commit()
    return __get_user(username)[1]


# Mushroom
def create_mushroom(name: str, family_id: str, season_start: str, season_end: str):
    """
    Add new mushroom to db

    :param name: str
    :param family_id: 'int', int as str
    :param season_start: 'int', int as str
    :param season_end: 'int', int as str

    :return:
        None
    """
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
    return db.session.execute(text('SELECT id, date, mushroom_id, location FROM sighting')).fetchall()


if "__name__" == "__main__":
    pass
