import os
import psycopg2
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

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
    # cur = conn.cursor()
    with conn.cursor() as cur:

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
                harvest_date DATE,
                publish_date TIMESTAMPTZ DEFAULT NOW(),
                location INTEGER,
                location_type INTEGER,
                location_modifier INTEGER,
                season INTEGER,
                rating INTEGER,
                notes TEXT
            );"""
        cur.execute(sql)
        sql = """
            CREATE TABLE location_modifier (
                id SERIAL PRIMARY KEY,
                name TEXT 
            );
        """
        cur.execute(sql)
        sql = """
            CREATE TABLE location_type (
                id SERIAL PRIMARY KEY,
                name TEXT
            );
        """
        cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def locations():
    conn = psycopg2.connect(f"dbname={os.getenv('DBNAME')} user={os.getenv('USER')}")
    with conn.cursor() as cur:
        modifiers = ["arid", "dry", "not weird at all", "wet", "underwater"]
        for mod in modifiers:
            sql = "INSERT INTO location_modifier (name) VALUES (%s)"
            cur.execute(sql, (mod,))
        types = ['coniferous forest', 'deciduous forest', 'mixed forest', 'field', 'grass', 'manure', 'swamp',
                 'concrete', 'volcanic glass']
        for typ in types:
            sql = "INSERT INTO location_type (name) VALUES (%s)"
            cur.execute(sql, (typ,))
    conn.commit()
    cur.close()
    conn.close()


def populate():
    # how many of each
    families = 10
    mushrooms = 25
    users = 30
    sightings = 1000

    conn = psycopg2.connect(f"dbname={os.getenv('DBNAME')} user={os.getenv('USER')}")
    with conn.cursor() as cur:
        sql = "INSERT INTO family (name) VALUES ('group'||generate_series(1, %s))"
        cur.execute(sql, (families,))
        conn.commit()

        sql = ("""
               INSERT INTO 
               mushroom (name, family_id, season_start, season_end) 
               VALUES 
               ('mushroom'||generate_series(1, %s), floor(random()* %s) + 1, floor(random()*8+1), floor(random()*4+8))
               """)
        cur.execute(sql, (mushrooms, families,))
        conn.commit()

        sql = "INSERT INTO account (username, password) VALUES (%s, %s)"
        for i in range(1, users + 1):
            cur.execute(sql, (f"username{i}", generate_password_hash(f"password{i}")))
        conn.commit()

        sql = """
                DROP FUNCTION IF EXISTS randy;
                CREATE FUNCTION randy(a INTEGER) RETURNS integer
                    IMMUTABLE
                    RETURNS NULL ON NULL INPUT 
                    RETURN FLOOR(RANDOM() * a)::INTEGER + 1;
                INSERT INTO 
                sighting (account_id, harvest_date, publish_date, mushroom_id, location, location_type, location_modifier, season, rating, notes) 
                VALUES 
                (randy(%s), 
                MAKE_DATE(2024, randy(6) + 6, randy(30)),
                CURRENT_TIMESTAMP(0) - (RANDOM() * '1 hour'::INTERVAL), 
                randy(%s), 
                randy(10000), 
                randy(9), 
                randy(5), 
                randy(12), 
                randy(10), 
                'very nice');
                DROP FUNCTION IF EXISTS randy;
                    """
        for i in range(sightings):
            cur.execute(sql, (users, mushrooms))
            conn.commit()
    conn.close()


def testeri():
    conn = psycopg2.connect(f"dbname={os.getenv('DBNAME')} user={os.getenv('USER')}")
    cur = conn.cursor()
    sql = "INSERT INTO account (username, password) VALUES ('user'||generate_series(1,20), 'password')"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def testeri2():
    conn = psycopg2.connect(f"dbname={os.getenv('DBNAME')} user={os.getenv('USER')}")
    cur = conn.cursor()
    with conn.cursor() as cursor:
        sql = """
            DROP FUNCTION IF EXISTS randy;
            CREATE FUNCTION randy(a INTEGER) RETURNS integer
                IMMUTABLE
                RETURNS NULL ON NULL INPUT 
                RETURN FLOOR(RANDOM() * a)::INTEGER; 
            INSERT INTO 
            sighting (account_id, harvest_date, publish_date, mushroom_id, location, location_type, location_modifier, season, rating, notes) 
            VALUES 
            (randy(10) + 1, 
            MAKE_DATE(2024, randy(6) + 7, randy(30) + 1),
            CURRENT_TIMESTAMP(0), 
            randy(20) + 1, 
            randy(10000) + 1, 
            randy(9) + 1, 
            randy(5) + 1, 
            randy(12) + 1, 
            randy(10) + 1, 
            'very nice');
            DROP FUNCTION IF EXISTS randy;
                """
        for i in range(10):
            cur.execute(sql, (10, 20))
            conn.commit()
    # cur.close()
    conn.close()
