from invoke import task
from mushroom_app.db_setup import drop_db_tables, create_db_tables, populate


# Alustukseen
@task
def clean(c):
    drop_db_tables()

@task
def tables(c):
    create_db_tables()

@task
def fill(c):
    populate()

@task
def build(c):
    print("Dropping tables")
    drop_db_tables()
    print("Creating new tables")
    create_db_tables()
    print("Fill her up!")
    populate()
    print("Done!")


@task
def start(c):
    c.run("flask --app mushroom_app/app run")
