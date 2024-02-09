import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()


def drop_db_tables():
    conn = psycopg2.connect(f"dbname={os.getenv('DBNAME')} user={os.getenv('USER')}")
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS sighting;")
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
                password TEXT
            );"""
    cur.execute(sql)
    sql = """
            CREATE TABLE sighting (
                id SERIAL PRIMARY KEY,
                account_id INTEGER REFERENCES account,
                mushroom_id INTEGER REFERENCES mushroom,
                date DATE,
                location INTEGER,
                location_type INTEGER,
                location_modifier INTEGER,
                season INTEGER,
                rating INTEGER,
                notes TEXT
            );"""
    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()


def populate():
    conn = psycopg2.connect(f"dbname={os.getenv('DBNAME')} user={os.getenv('USER')}")
    cur = conn.cursor()
    sql = "INSERT INTO family (name) VALUES ('strain'||generate_series(1,10))"
    cur.execute(sql)
    conn.commit()
    sql = "INSERT INTO mushroom (name, family_id, season_start, season_end) VALUES ('mushroom'||generate_series(1,20), floor(random()*10) + 1, floor(random()*8+1), floor(random()*4+8))"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
