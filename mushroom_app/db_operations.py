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


def get_user_list():
    sql = "SELECT id,username FROM account"
    return db.session.execute(text(sql)).fetchall()


def get_account_info(id_to_look_for: int):
    print(id_to_look_for)
    pass


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
    sql = text("""
    INSERT INTO 
    mushroom (name, family_id, season_start, season_end) 
    VALUES (:name, :family_id, :season_start, :season_end)
    """)
    db.session.execute(sql, {"name": name, "family_id": family_id,
                             "season_start": season_start, "season_end": season_end})
    db.session.commit()


def get_mushrooms():
    sql = "SELECT M.name, F.name,M.season_start, M.season_end FROM mushroom M JOIN family F ON M.family_id = F.id"
    return db.session.execute(text(sql)).fetchall()


# Family
def get_family_list():
    sql = "SELECT id, name FROM family"
    return db.session.execute(text(sql)).fetchall()


def create_family(family_name):
    # TODO
    pass


# Sightings
def get_sightings():
    sql = "SELECT S.id, S.harvest_date, M.name, S.location FROM sighting S JOIN mushroom M ON S.mushroom_id = M.id"
    return db.session.execute(text(sql)).fetchall()


def get_new_sightings():
    show_limit = 20
    sql = """
    SELECT S.id, S.harvest_date, M.name, S.location 
    FROM sighting S JOIN mushroom M 
    ON S.mushroom_id = M.id 
    ORDER BY S.publish_date DESC LIMIT %s
    """
    return db.session.execute(text(sql), (show_limit,)).fetchall()


def create_sighting(account_id: int,mushroom_id: int, harvest_date: str, location: int, location_type: int,
                    location_modifier: int, rating: int, notes: str):
    sql = """
    INSERT INTO sighting
    (account_id, mushroom_id, harvest_date,publish_date, location, location_type, location_modifier, rating, notes)
    VALUES 
    (:account_id, :mushroom_id, :harvest_date, NOW(), :location, :location_type, 
    :location_modifier, :rating, :notes)
    """
    values = {account_id: 1, mushroom_id: mushroom_id, harvest_date: harvest_date, location: location,
              location_type: location_type, location_modifier: location_modifier, rating: rating, notes: notes}
    db.session.execute(text(sql), values)
    db.session.commit()


if "__name__" == "__main__":
    pass
