# -*- coding: utf-8 -*-

from flask import Flask, jsonify, g,render_template
from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
import pymysql.cursors
from flask_login import LoginManager
from flask import Response, current_app, abort
from pymysql import MySQLError
from config import *

from os import listdir
from os.path import isfile, join
import os.path

def create_app(config_obj_str):
    app = Flask(__name__)
    app.config.from_object(config_obj_str) 
    CORS(app, resources={r'/*': {'origins': '*'}})
    
    @app.teardown_appcontext
    def teardown_db(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()         
    
    from backend.auth import auth_bp, authentication
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from backend.search import search_bp
    app.register_blueprint(search_bp, url_prefix='/search')
    from backend.film import film_bp
    app.register_blueprint(film_bp, url_prefix='/film')
    from backend.comment import comment_bp
    app.register_blueprint(comment_bp, url_prefix='/comment')
    from backend.blocklist import blocklist_bp
    app.register_blueprint(blocklist_bp, url_prefix='/blocklist')
    from backend.wishlist import wishlist_bp
    app.register_blueprint(wishlist_bp, url_prefix='/wishlist')
    
    @app.route('/<path:fallback>')
    def fallback(fallback):       # Vue Router 的 mode 为 'hash' 时可移除该方法
        if fallback.startswith('css/') or fallback.startswith('js/')\
            or fallback.startswith('img/') or fallback == 'favicon.ico':
                return app.send_static_file(fallback)
        else:
            return app.send_static_file('index.html')
    
    # flask-login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "/"

    # handle login failed
    @app.errorhandler(401)
    def errorhandler_401(e):
        return jsonify({"login_status":0})  
        
        
    # callback to reload the user object        
    @login_manager.user_loader
    def load_user(userid):
        try:
            sql = ("SELECT `users`.`user_id`,`users`.`username`,`users`.`nick_name`, `users`.`age`,`users`."
                "`gender`,`users`.`street`,`users`.`suberb`,`users`.`city`,`users`.`postcode`,`users`.`description`"
                "FROM `filmfinder`.`users`"
                "Where user_id = %s")
            db = get_db(current_app)
            with db.cursor() as c:
                # print(sql%userid)
                c.execute(sql,(userid))
                  
            return authentication.User(**c.fetchone())    
        except MySQLError as err:
            print(err)
        return abort(500) 

    return app  

def get_db(app):
    if 'db' not in g or not g.db.open:
        config = {
              'user': app.config['DB_USER'],
              'password': app.config['DB_PASSWORD'],
              'host': app.config['DB_HOSTNAME'],
              'db': app.config['DB_SCHEMA']
            }
        g.db = pymysql.connect(**config,
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=False)
        if g.db.open:
            print("DB is Connected")
        else:
            print("DB is not connected")
    return g.db

def printR(request):
    print("---headers")
    print(request.headers)
    print("---data")
    print(request.data)
    print("---args")
    print(request.args)
    print("---form")
    print(request.form)
    print("---json")
    print(request.json)
    print("---values")
    print(request.values)
    print("---endpoint")
    print(request.endpoint)
    print("---method")
    print(request.method)
    print("---remote_addr")
    print(request.remote_addr)
    print("---")
