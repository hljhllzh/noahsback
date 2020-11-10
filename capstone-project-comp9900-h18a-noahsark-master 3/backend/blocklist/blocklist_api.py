# -*- coding: utf-8 -*-

from . import blocklist_bp
from flask_login import  login_required,current_user
from flask import request, current_app,abort,jsonify,make_response
from backend import printR,get_db
from pymysql import escape_string, MySQLError
    
@blocklist_bp.route('/add_blocklist', methods=['POST'])
@login_required
def add_blocklist():
    if "user_id" in request.form and current_user.get_id() != request.form['user_id']:
        try:
            db = get_db(current_app)
            with db.cursor() as c:
                sql = " INSERT INTO `filmfinder`.`blocklist`(`user_id`,`blocklisted_user`) VALUES (%s,%s);"
                print(sql%(current_user.get_id(),request.form['user_id']))
                c.execute(sql,(current_user.get_id(),request.form['user_id']))
            db.commit()
        except MySQLError as err:
            db.rollback()
            print(err)
        else:
            return f"OK",200
    abort(400)

#TODO -- return user info instead of ids
@blocklist_bp.route('/get_blocklist', methods=['GET'])
@login_required
def get_blocklist():
    if "page" in request.args and "page_size" in request.args:
        size = 50
        if "page_size" in request.args:
            size = int(escape_string(request.args['page_size']))
            if size >50:
                size = 50
        limit = f"limit {size}"
        if "page" in request.args:
            offset = (int(escape_string(request.args['page'])) -1 )* size
            limit += f" OFFSET {offset}"
        try:
            
            db = get_db(current_app)
            with db.cursor() as c:
                sql = f""" SELECT `users`.`user_id`,
                    `users`.`username`,
                    `users`.`nick_name`,
                    `users`.`age`,
                    `users`.`gender`,
                    `users`.`street`,
                    `users`.`suberb`,
                    `users`.`city`,
                    `users`.`postcode`,
                    `users`.`description` 
                    from `filmfinder`.`blocklist` as b left join `filmfinder`.`users`  on b.blocklisted_user = users.user_id  where b.user_id = %s {limit};"""
                print(sql%(current_user.get_id()))
                c.execute(sql,(current_user.get_id()))
                result = c.fetchall()
                return jsonify(result)
        except MySQLError as err:
            db.rollback()
            print(err)
        else:
            return f"OK",200
    abort(400)
    
@blocklist_bp.route('/rm_blocklist', methods=['POST'])
@login_required
def rm_blocklist():
    if "user_id" in request.form:
        try:
            db = get_db(current_app)
            with db.cursor() as c:
                sql = "DELETE FROM `filmfinder`.`blocklist` WHERE user_id = %s and blocklisted_user = %s;"
                # print(sql%(rows,values))
                c.execute(sql,(current_user.get_id(),request.form['user_id']))
            db.commit()
        except MySQLError as err:
            db.rollback()
            print(err)
        else:
            return f"OK",200
    abort(400)