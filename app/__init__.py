"""from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager 

db = SQLAlchemy() 
login_manager = LoginManager() 

def create_app():
     
  app = Flask(__name__) 
  app.config['SECRET_KEY'] = 'demo-secret-key' 
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' 
  
  db.init_app(app) 
  login_manager.init_app(app) 
  login_manager.login_view = 'auth.login' 
  # Import and register blueprints 
  from .routes import main as main_blueprint 
  app.register_blueprint(main_blueprint) 
  
  from .auth import auth as auth_blueprint 
  app.register_blueprint(auth_blueprint) 
  return app"""
  
  # app/__init__.py
import os
from flask import Flask
from flask_login import LoginManager
from .database import db, User   # import db from database.py (single source)
 
login_manager = LoginManager()

def create_app(config: dict | None = None):
    app = Flask(__name__, instance_relative_config=True)

    # default config - you can keep your existing settings
    app.config.setdefault("SECRET_KEY", "demo-secret-key")
    # store sqlite inside instance for safer local/CI handling
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///instance/users.db")

    if config:
        app.config.update(config)

    # ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # register blueprints (unchanged)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
