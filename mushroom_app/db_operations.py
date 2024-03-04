from sqlalchemy.sql import text
from app import db
from werkzeug.security import check_password_hash, generate_password_hash


# Account
def __get_user(username: str):
    """
    Get userrow by username

    :param username: string
    :return:
        Row(id, name, password)
    """
    sql = text("SELECT * FROM Account WHERE username = :username")
    return db.session.execute(sql, {"username": username}).fetchone()


def __get_account(user_id: int):
    """
    Get account info by user_id

    :param user_id: int
    :return:
        Row(id, username)
    """
    sql = text("SELECT id,username FROM Account WHERE id = :user_id")
    return db.session.execute(sql, {"user_id": user_id}).fetchone()


def check_user(username: str, password: str) -> str:
    """
    Check password against password hash

    :param username:
    :param password:
    :return:
        username or ""
    """
    user_id, username, password_hash = __get_user(username)
    if check_password_hash(password_hash, password):
        return username
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
    return __get_account(id_to_look_for)


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


def get_mushrooms_list():
    sql = """
        SELECT M.id, M.name, F.id AS family_id, F.name AS family_name, COUNT(S.id) AS amount 
        FROM mushroom M LEFT JOIN sighting S ON M.id = S.mushroom_id LEFT JOIN family F ON M.family_id = F.id 
        GROUP BY M.id, F.id;
    """
    return db.session.execute(text(sql)).fetchall()


def get_mushroom(mushroom_id: int):
    sql = ("""
            SELECT M.name, M.family_id, F.name AS family_name, M.season_start, M.season_end 
            FROM mushroom m JOIN family F ON M.family_id = F.id 
            WHERE m.id=:mushroom_id
           """)
    return db.session.execute(text(sql), {"mushroom_id": mushroom_id}).fetchone()


def get_family_members(family_id: int):
    sql = """
    SELECT M.id, M.name, COUNT(S.id) AS amount 
    FROM mushroom M LEFT JOIN sighting S on M.id = S.mushroom_id
    WHERE family_id=:family_id
    GROUP BY M.id
    """
    return db.session.execute(text(sql), {"family_id": family_id}).fetchall()


# Family
def get_family_list():
    sql = """
        WITH amounts AS
        (SELECT M.family_id, COUNT(*) AS amount FROM mushroom M GROUP BY family_id)
        SELECT F.id, F.name, A.amount 
        FROM family F JOIN amounts A ON A.family_id = F.id
            """
    return db.session.execute(text(sql)).fetchall()


def get_family(family_id: int):
    sql = "SELECT id,name FROM family WHERE id=:family_id"
    return db.session.execute(text(sql), {"family_id": family_id}).fetchone()


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
    SELECT S.id, M.name, S.harvest_date, S.location, S.rating
    FROM sighting S JOIN mushroom M 
    ON S.mushroom_id = M.id 
    ORDER BY S.publish_date DESC 
    LIMIT :show_limit
    """
    return db.session.execute(text(sql), {"show_limit": show_limit}).fetchall()


def get_last_sighting_by_mushroom_id(mushroom_id: int, limit: int = 5):
    """
    get :limit last by :harvest_date sighting of :mushroom_id
    :param mushroom_id:
    :param limit:
    :return:
        Row (id, harvest_date, name, location, location_type, location_modifier, rating)
    """
    sql = """
    SELECT S.id, S.harvest_date, M.name, S.account_id, A.username AS account_name, S.location, 
    T.name AS location_type, location_modifier.name AS location_modifier, S.rating 
    FROM sighting S 
    JOIN mushroom M on S.mushroom_id = M.id
    JOIN account A on S.account_id = A.id
    JOIN location_type T ON S.location_type = T.id
    JOIN location_modifier ON S.location_modifier = location_modifier.id
    WHERE S.mushroom_id = :mushroom_id
    ORDER BY harvest_date DESC 
    LIMIT :limit"""
    return db.session.execute(text(sql), {"mushroom_id": mushroom_id, "limit": limit}).fetchall()


def get_top_sighting_by_mushroom_id(mushroom_id: int, limit: int = 5):
    """
    get :limit best by :rating sightings of :mushroom_id
    :param mushroom_id: id in table mushroom
    :param limit: return this many sightings
    :return:
        Row(id, harvest_date, mushroom_name, location, location_type, location_modifier, rating)
    """
    sql = """
    SELECT S.id, S.harvest_date, M.name AS mushroom_name, S.location, T.name AS location_type, 
    location_modifier.name AS location_modifier, S.rating, M.family_id, F.name AS family_name
    FROM sighting S JOIN mushroom M on S.mushroom_id = M.id LEFT JOIN family F ON M.family_id = F.id
    JOIN location_modifier ON location_modifier.id = S.location_modifier
    JOIN location_type T ON S.location_type = T.id
    WHERE mushroom_id =:mushroom_id 
    ORDER BY rating DESC, harvest_date DESC 
    LIMIT :limit
    """
    return db.session.execute(text(sql), {"mushroom_id": mushroom_id, "limit": limit}).fetchall()


def get_last_sighting_by_account_id(account_id: int, limit: int = 5):
    """
    get :limit last sightings made by :account_id
    :param account_id:
    :param limit:
    :return:
        Row(id, mushroom_id, mushroom_name, mushroom_family, harvest_date, location, location_type,
            location_modifier, rating)
    """
    sql = """
    SELECT S.id, S.mushroom_id, M.name AS mushroom_name, F.name AS mushroom_family, 
        S.harvest_date, S.location, T.name AS location_type,  location_modifier.name AS location_modifier, 
        S.rating  
    FROM sighting S JOIN mushroom M ON S.mushroom_id = M.id LEFT JOIN family F on M.family_id = F.id
    JOIN location_type T ON S.location_type = T.id
    JOIN location_modifier ON S.location_modifier = location_modifier.id 
    WHERE account_id=:account_id ORDER BY harvest_date DESC LIMIT :limit
    """
    return db.session.execute(text(sql), {"account_id": account_id, "limit": limit}).fetchall()


def get_sighting(sighting_id: int):
    sql = """
    SELECT S.id, M.name AS mushroom_name, S.mushroom_id, M.family_id, F.name AS family_name, 
    S.account_id, A.username AS account_name, S.harvest_date, S.publish_date, S.location, 
    T.name AS location_type, location_modifier.name AS location_modifier, S.rating, S.notes 
    FROM sighting S 
    JOIN mushroom M ON S.mushroom_id = M.id 
    JOIN family F ON M.family_id = F.id
    JOIN account A ON S.account_id = A.id
    JOIN location_type T ON S.location_type = T.id
    JOIN location_modifier ON S.location_modifier = location_modifier.id
    WHERE S.id = :sighting_id"""
    return db.session.execute(text(sql), {"sighting_id": sighting_id}).fetchone()


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
