from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
import os


def _get_db_context():
    app = Flask(__name__)
    load_dotenv()
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///" + os.getenv("DBNAME")
    db = SQLAlchemy(app)
    return app, db


def drop_db_tables():
    app, db = _get_db_context()
    with app.app_context():
        db.session.execute(text("DROP TABLE IF EXISTS sighting"))
        db.session.execute(text("DROP TABLE IF EXISTS account"))
        db.session.execute(text("DROP TABLE IF EXISTS mushroom"))
        db.session.execute(text("DROP TABLE IF EXISTS family"))
        db.session.execute(text("DROP TABLE IF EXISTS location_modifier"))
        db.session.execute(text("DROP TABLE IF EXISTS location_type"))
        db.session.commit()


def create_db_tables():
    app, db = _get_db_context()
    with app.app_context():
        sql = """CREATE TABLE family (
                    id SERIAL PRIMARY KEY, 
                    name TEXT
                    )"""
        db.session.execute(text(sql))
        sql = """CREATE TABLE mushroom (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    family_id INTEGER REFERENCES family,
                    season_start INTEGER,
                    season_end INTEGER
                    )"""
        db.session.execute(text(sql))
        sql = """CREATE TABLE account (
                    id SERIAL PRIMARY KEY,
                    username TEXT,
                    password TEXT
                    )"""
        db.session.execute(text(sql))
        sql = """CREATE TABLE sighting (
                    id SERIAL PRIMARY KEY,
                    account_id INTEGER REFERENCES account,
                    mushroom_id INTEGER REFERENCES mushroom,
                    harvest_date DATE,
                    publish_date TIMESTAMPTZ DEFAULT NOW(),
                    location INTEGER,
                    location_type INTEGER,
                    location_modifier INTEGER,
                    season INTEGER,
                    rating INTEGER,
                    notes TEXT
                    )"""
        db.session.execute(text(sql))
        db.session.commit()


def populate():
    # how many of each
    amounts = {'families': 10, 'mushrooms': 25, 'users': 30, 'sightings': 1000}

    app, db = _get_db_context()

    with app.app_context():
        sql = """INSERT INTO family (name) VALUES ('group'||generate_series(1, :families))"""
        db.session.execute(text(sql), {**amounts})
        db.session.commit()
        print("family done")

        sql = """INSERT INTO 
                   mushroom (name, family_id, season_start, season_end) 
                   VALUES 
                   ('mushroom'||generate_series(1, :mushrooms), 
                   floor(random()* :families) + 1, 
                   floor(random()*8+1), 
                   floor(random()*4+8))
                   """
        db.session.execute(text(sql), {**amounts})
        db.session.commit()
        print("mushroom done")

        sql = """INSERT INTO account (username, password) VALUES (:username, :password)"""
        for i in range(1, amounts['users'] + 1):
            db.session.execute(text(sql), {'username': f"username{i}", 'password': generate_password_hash(f"password{i}")})
        db.session.commit()
        print("account done")

        sql = """DROP FUNCTION IF EXISTS randymizer;
                    CREATE FUNCTION randymizer(a INTEGER) RETURNS integer
                        IMMUTABLE
                        RETURNS NULL ON NULL INPUT 
                        RETURN FLOOR(RANDOM() * a)::INTEGER + 1;
                        """
        db.session.execute(text(sql))
        db.session.commit()
        sql = """INSERT INTO 
                    sighting (account_id, harvest_date, publish_date, mushroom_id, location, location_type, 
                                location_modifier, season, rating, notes) 
                    VALUES 
                    (randymizer(:users), 
                    MAKE_DATE(2023, randymizer(6) + 6, randymizer(30)),
                    CURRENT_TIMESTAMP(0) - (RANDOM() * '1 hour'::INTERVAL), 
                    randymizer(:mushrooms), 
                    randymizer(10000), 
                    randymizer(9), 
                    randymizer(5), 
                    randymizer(12), 
                    randymizer(10), 
                    'very nice')
                    """
        for i in range(amounts['sightings']):
            db.session.execute(text(sql), {**amounts})
        sql = "DROP FUNCTION IF EXISTS randymizer"
        db.session.execute(text(sql))
        db.session.commit()
        print("sighting done")


def populate2():
    """
    Populate the database with simple example data.

    Defines, makes heavy use of, and drops the randymizer SQL function on server.

    :return:
    """
    # how many of each
    families = 10
    mushrooms = 25
    users = 30
    sightings = 1000

    app, db = _get_db_context()

    with app.app_context():
        # define function in database
        sql = """DROP FUNCTION IF EXISTS randymizer;
                            CREATE FUNCTION randymizer(a INTEGER) RETURNS integer
                                IMMUTABLE
                                RETURNS NULL ON NULL INPUT 
                                RETURN FLOOR(RANDOM() * a)::INTEGER + 1;
                                """
        db.session.execute(text(sql))
        db.session.commit()

        sql = "INSERT INTO family (name) VALUES (:name)"
        for i in range(1, families + 1):
            db.session.execute(text(sql), {'name': f'group{i}'})
        db.session.commit()

        sql = """  INSERT INTO 
                   mushroom (name, family_id, season_start, season_end) 
                   VALUES 
                   (:name, 
                   randymizer(:families), 
                   randymizer(8), 
                   randymizer(4) + 7
                   )"""
        for i in range(1, mushrooms + 1):
            db.session.execute(text(sql), {'name': f'mushroom{i}', 'families': families})
        db.session.commit()

        sql = """INSERT INTO account (username, password) VALUES (:username, :password)"""
        for i in range(1, users + 1):
            db.session.execute(text(sql), {'username': f"username{i}",
                                           'password': generate_password_hash(f"password{i}")})
        db.session.commit()

        sql = """   INSERT INTO 
                    sighting (account_id, harvest_date, publish_date, mushroom_id, location, location_type, 
                                location_modifier, season, rating, notes) 
                    VALUES 
                    (randymizer(:users), 
                    MAKE_DATE(2023, randymizer(6) + 6, randymizer(30)),
                    CURRENT_TIMESTAMP(0) - (RANDOM() * '1 hour'::INTERVAL), 
                    randymizer(:mushrooms), 
                    randymizer(10000), 
                    randymizer(9), 
                    randymizer(5), 
                    randymizer(12), 
                    randymizer(10), 
                    'very nice')
                    """
        for i in range(1, sightings + 1):
            db.session.execute(text(sql), {'users': users, 'mushrooms': mushrooms})
        db.session.commit()

        # cleanup function in database
        sql = "DROP FUNCTION IF EXISTS randymizer"
        db.session.execute(text(sql))
        db.session.commit()


