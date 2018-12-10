# app will be accessible through the import, therefore enabling run:app
# declared in uwsgi.ini
from app import app
from db import db


@app.before_first_request
def create_tables():
    # Magic functionality knows table structure from importing model libs
    # at run-time
    db.create_all()


db.init_app(app)
