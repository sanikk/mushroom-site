# Mushroom site

## A simple site for reporting your mushroom finds.

Written as school project for TSoHa.

Installation instructions:

1. Have postgresql installed and ready to use
2. You need an .env file with these keys filled with a valid 
   postgresql database name and user, respectively. And a secret key for
   sessions.  
```text
DBNAME =
USER =
SECRET_KEY = 
```
   You can generate a secret key with
```bash
python -c 'import secrets;print(secrets.token_hex(16))'
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
poetry run invoke start
```

