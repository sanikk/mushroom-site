# Mushroom site

## A simple site for reporting your mushroom finds.

Written as school project for TSoHa.

Installation instructions:

1. Have postgresql installed and ready to use
2. You need an .env file with these two keys filled with a valid 
   postgresql database name and user, respectively.
```text
DBNAME=
USER=
```
3. install required libraries
```bash
poetry install
```
4. create the database tables

```bash
poetry run invoke build
```
5. launch the server
```bash
poetry run flask run
```

