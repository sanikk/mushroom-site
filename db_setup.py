import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()


def drop_db_tables():
    conn = psycopg2.connect(f"dbname={os.getenv('DBNAME')} user={os.getenv('USER')}")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS account;")
    cur.execute("DROP TABLE IF EXISTS mushroom;")
    cur.execute("DROP TABLE IF EXISTS family;")
    conn.commit()
    cur.close()
    conn.close()


def create_db_tables():
    conn = psycopg2.connect(f"dbname={os.getenv('DBNAME')} user={os.getenv('USER')}")
    cur = conn.cursor()
    sql = "CREATE TABLE family (id SERIAL PRIMARY KEY, name TEXT);"
    cur.execute(sql)
    sql = """CREATE TABLE mushroom (
            id SERIAL PRIMARY KEY,
            name TEXT,
            family_id INTEGER REFERENCES family,
            season_start INTEGER,
            season_end INTEGER
            );"""
    cur.execute(sql)
    sql = """
            CREATE TABLE account (
                id SERIAL PRIMARY KEY,
                username TEXT,
                name TEXT,
                password TEXT
            );"""
    cur.execute(sql)
    sql = """
            CREATE TABLE sighting (
                id SERIAL PRIMARY KEY,
                account_id INTEGER REFERENCES account,
                mushroom_id INTEGER REFERENCES mushroom,
                location TEXT,
                location_type TEXT,
                location_modifier TEXT,
                season INTEGER,
                rating INTEGER,
                notes TEXT
            );"""
    conn.commit()
    cur.close()
    conn.close()


def populate():
    conn = psycopg2.connect(f"dbname={os.getenv('DBNAME')} user={os.getenv('USER')}")
    cur = conn.cursor()
    sql = "INSERT INTO family (name) VALUES ('Tatit')"
    cur.execute(sql)
    sql = "INSERT INTO mushroom (name, family_id, season_start, season_end) VALUES ('Herkkutatti', 1,6,10)"
    cur.execute(sql)
    #dbtex("INSERT INTO family (name) VALUES ('Rouskut')")
    #dbtex("INSERT INTO family (name) VALUES ('Haperot')")
    #dbtex("INSERT INTO family (name) VALUES ('Käävät')")
    conn.commit()
    cur.close()
    conn.close()

