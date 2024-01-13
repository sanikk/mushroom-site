from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy


# init
load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///" + os.getenv("DBNAME")
db = SQLAlchemy(app)


# circular import, ugly
import routes