from flask import Flask
import config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap  import Bootstrap

db = SQLAlchemy()

def createapp():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
    app.secret_key = config.SECRET
    db.init_app(app)
    return app

app = createapp()
bootstrap = Bootstrap(app)

import tables
import main.views

#db.create_all()

