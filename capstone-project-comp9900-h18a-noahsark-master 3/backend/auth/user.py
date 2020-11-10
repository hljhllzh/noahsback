# -*- coding: utf-8 -*-

from . import auth_bp
from backend import get_db
from flask import request, jsonify, current_app,abort,redirect
from pymysql import escape_string, MySQLError
from passlib.hash import pbkdf2_sha512
from flask_login import  login_required, current_user, login_manager, logout_user

@auth_bp.route('/create_user', methods=['POST'])
def create_user():
    ks = {'username','password','nick_name','age','gender','street',\
          'suberb','city','postcode','description'}
    if set(request.form.keys()).issuperset(ks) and request.form["username"] and  request.form["password"] :
        rows = ""
        values = ""
        for k in ks:
            rows += f"`{k}`,"
            if k == 'age' or k == 'gender':
                v = escape_string(request.form[k])
                values += f"{v if v else 'NULL'},"
            elif k == 'password':
                hash = pbkdf2_sha512.hash(request.form[k])
                values += f"'{hash}',"
            else:
                values += f"'{escape_string(request.form[k])}',"
        rows = rows[:-1] 
        values = values[:-1] 
        try:
            db = get_db(current_app)
            with db.cursor() as c:
                sql = " INSERT INTO `filmfinder`.`users`(%s) VALUES (%s);"
                print(sql%(rows,values))
                c.execute(sql%(rows,values))
            db.commit()
        except MySQLError as err:
            db.rollback()
            print(err)
        else:
            return f"OK",200
    abort(400)

#if password is updated, redirect to the login page    
@auth_bp.route('/update_user', methods=['POST'])
@login_required
def update_user():
    print(current_app.login_manager.login_view)
    ks = {'username','password','nick_name','age','gender','street',\
          'suberb','city','postcode','description'}
    if ks.issuperset(set(request.form.keys())):
        values = ""
        for k in request.form.keys():
            if k == 'age' or k == 'gender':
                v = escape_string(request.form[k])
                values += f"{k} = {v if v else 'NULL'},"
            elif k == 'password':
                hash = pbkdf2_sha512.hash(request.form[k])
                values += f"{k} = '{hash}',"
            else:
                values += f"{k} = '{escape_string(request.form[k])}',"
        values = values[:-1] 
        try:
            db = get_db(current_app)
            with db.cursor() as c:
                sql = " UPDATE `filmfinder`.`users` SET %s WHERE user_id = '%s';"
                print(sql%(values,current_user.get_id()))
                c.execute(sql%(values,current_user.get_id()))
            db.commit()
        except MySQLError as err:
            db.rollback()
            print(err)
        else:
            if "password" in  request.form.keys():
                logout_user()
                return redirect(current_app.login_manager.login_view)
            else:
                return f"OK",200
    abort(400)

@auth_bp.route('/check_username', methods=['GET'])
def check_username():
    if request.args["username"]:
        try:
            db = get_db(current_app)
            with db.cursor() as c:
                sql = "select 1 from `filmfinder`.`users` where username = %s;"
                c.execute(sql,request.args["username"])
                if c.rowcount==1:
                    return jsonify({"confict_name":1})
                else:
                    return jsonify({"confict_name":0})
        except MySQLError as err:
            print(err)
    abort(400)

@auth_bp.route('/current_user', methods=['GET'])
@login_required
def get_user():
    print(current_user.get_id())
    return jsonify(current_user.__dict__)

@auth_bp.route('/user/<user_id>', methods=['GET'])
@login_required
def get_user_by_id(user_id):
    try:
        sql = ("SELECT `users`.`user_id`,`users`.`username`,`users`.`nick_name`, `users`.`age`,`users`."
            "`gender`,`users`.`street`,`users`.`suberb`,`users`.`city`,`users`.`postcode`,`users`.`description`"
            "FROM `filmfinder`.`users`"
            "Where user_id = %s")
        db = get_db(current_app)
        with db.cursor() as c:
            c.execute(sql,(user_id))
              
        return jsonify(c.fetchone())    
    except MySQLError as err:
        print(err)
    return abort(500) 