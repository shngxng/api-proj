from flask import Flask
from flask_migrate import Migrate
from app.database import db
from flask_sqlalchemy import SQLAlchemy
from app.models import User, Case
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager
from .routes.auth import auth_ns
from .routes.cases import case_ns
from flask.cli import with_appcontext
import os

from flask_restx import Api

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('', 'db.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # migrate.init_app(app, db)
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    api = Api(app, 
              title="Mental Health API", 
              version="1.0", 
              description="API for clinicians to manage therapy cases", 
              security="Bearer Auth",  
              authorizations={
                  "Bearer Auth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                    "description": "Add 'Bearer <JWT_TOKEN>' in the Authorization header"
                    }
                })
    api.add_namespace(case_ns)
    api.add_namespace(auth_ns)
    
    # Seed data inside the application context
    with app.app_context():
        # print("seeding database")
        db.create_all()  
        seed_data()
    
    return app


def seed_data():
    # Add users
    if not User.query.first():
        # print("hello")
        db.session.add(User(username="joel87", password=generate_password_hash("pwjoel87"), first_name="Joel", last_name="Tan", role="Senior"))
        db.session.add(User(username="shiminh", password=generate_password_hash("pwshiminh"), first_name="Shimin", last_name="Huang", role="Junior"))
        db.session.add(User(username="rishiaw", password=generate_password_hash("pwrishiaw"), first_name="Rishi", last_name="Agarwal", role="Junior"))
        
    # Add cases
    if not Case.query.first():
        db.session.add(Case(name="Jonathan Lim", description="A 28-year-old software engineer who is experiencing intense anxiety during team meetings and is struggling to speak up, fearing judgment from colleagues."))
        db.session.add(Case(name="Angela Paolo", description="A 42-year-old teacher who is coping with the recent loss of a parent and is finding it difficult to concentrate on work and daily responsibilities."))
        db.session.add(Case(name="Xu Yaoming", description="A 16-year-old high school student who is feeling overwhelmed by academic pressure and is struggling to balance schoolwork, extracurriculars, and personal time."))

    db.session.commit()

