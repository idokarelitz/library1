from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#initialize the database
db= SQLAlchemy()
migrate=Migrate()