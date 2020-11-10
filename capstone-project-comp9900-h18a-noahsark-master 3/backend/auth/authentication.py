# -*- coding: utf-8 -*-

from . import auth_bp
from flask_login import  UserMixin, login_required, login_user, logout_user 
from flask import request, current_app,abort,jsonify,make_response
from backend import printR,get_db
from pymysql import escape_string, MySQLError
from passlib.hash import pbkdf2_sha512

# silly user model
class User(UserMixin):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
    def __repr__(self):
        return self.__dict__
    
    def get_id(self):
           return (self.user_id)

@auth_bp.route('/', methods=["GET"])
def index():
    resp = make_response()
    # redirect to a page that display the cookie
    resp.headers['data'] = "fk"
    resp.set_cookie('somecookiename', 'I am cookie')
    return resp 

# somewhere to login
@auth_bp.route("/login", methods=["POST"])
def login():
    if request.form["username"] and request.form["password"]:
        try:
            sql = ("SELECT `users`.`user_id`,`users`.`password`,`users`.`username`,`users`.`nick_name`, `users`.`age`,`users`."
                "`gender`,`users`.`street`,`users`.`suberb`,`users`.`city`,`users`.`postcode`,`users`.`description`"
                "FROM `filmfinder`.`users`"
                "Where username = %s;")
            db = get_db(current_app)
            name = escape_string(request.form["username"])
            with db.cursor() as c:
                print(sql%name)
                c.execute(sql,name)
                if c.rowcount==1:  
                    row = c.fetchone()
                    if  pbkdf2_sha512.verify(request.form["password"], row['password']):
                        user = User(**row) 
                        login_user(user) 
                        return jsonify({"login_status":1})  
        except MySQLError as err:
            print(err)
    abort(401)
    
@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"login_status":0})  

