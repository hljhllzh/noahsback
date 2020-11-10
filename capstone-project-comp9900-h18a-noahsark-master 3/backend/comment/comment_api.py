# -*- coding: utf-8 -*-

from . import comment_bp
from flask_login import  login_required,current_user
from flask import request, current_app,abort,jsonify,make_response
from backend import printR,get_db
from pymysql import escape_string, MySQLError

@comment_bp.route('/add_response', methods=["POST"])
@login_required
def add_response():
    printR(request)
    """
    Description
    -----------
    this function add response to other commnet
    
    Parameter
    ---------
    @response_id: responding to which comment. It must not be empty.
    @comment: comment text.It must not be empty.
    @ancestor_comment_id: under which rated comment
    
    Returns
    -------
    "Ok", 200
    "bad request", 400

    """
    if {'response_id','comment'} == set(request.form.keys()):
        for k in {'response_id','comment'}:
            if not request.form[k]:
                abort(400)
        comment_values = ""
        comment_values += f"'{escape_string(current_user.get_id())}',"
        # comment_values += f"{escape_string(request.form['movie_id'])},"
        comment_values += f"'{escape_string(request.form['comment'])}'"
        # comment_values += f"{escape_string(request.form['ancestor_comment_id'])}"
        try:
            db = get_db(current_app)
            with db.cursor() as c:
                #insert cooment
                sql = f" INSERT INTO `filmfinder`.`userXcomment`(user_id,comment,ancestor_comment_id) select %s,ancestor_comment_id from filmfinder.userXcomment where comment_id = {request.form['response_id']};"
                print(sql%(comment_values))
                c.execute(sql%(comment_values))
                
                #insert response relationship
                sql = " INSERT INTO `filmfinder`.`commentXresponse`(comment_id,response_to) VALUES (%s,%s);"
                
                print(sql%(c.lastrowid,request.form['response_id']))
                c.execute(sql%(c.lastrowid,request.form['response_id']))
 
        except MySQLError as err:
            db.rollback()
            print(err)
        else:
            db.commit()
            return f"OK",200
    abort(400)

@comment_bp.route('/add_comment', methods=["POST"])
@login_required
def add_comment():
    """
    Description
    -----------
    this function add comment which comes with rating.
    And it requires login in.
    each user can only rate a movie once
    
    Parameter
    ---------
    @movie_id: which movie mush not be empty
    @rating: the rating of the movie must not be empty
    @comment: comment mush not be empty
    
    Returns
    -------
    "Ok", 200
    "bad request", 400

    """
    if {'movie_id','rating','comment'} == set(request.form.keys()):
        for k in {'movie_id','rating','comment'}:
            if not request.form[k]:
                abort(400)
        rating_values = ""
        rating_values += f"'{escape_string(current_user.get_id())}',"
        rating_values += f"{escape_string(request.form['movie_id'])},"
        if request.form['rating']: 
            rating_values += f"{escape_string(request.form['rating'])}"
        else:
            rating_values += "NULL"
            
        
        comment_values = ""
        comment_values += f"'{escape_string(current_user.get_id())}',"
        # comment_values += f"{escape_string(request.form['movie_id'])},"
        if  request.form['comment']: 
            comment_values += f"'{escape_string(request.form['comment'])}'"
        else:
            comment_values += "''"

        try:
            db = get_db(current_app)
            with db.cursor() as c:
                #insert comment
                sql = " INSERT INTO `filmfinder`.`userXcomment`(user_id,comment) VALUES (%s);"
                print(sql%(comment_values))
                c.execute(sql%(comment_values))
                
                last_id = c.lastrowid
                sql = f"""update `filmfinder`.`userXcomment`
                        set ancestor_comment_id = {last_id}
                        where comment_id = {last_id};
                        """
                c.execute(sql)
                #insert rating
                sql = f" INSERT INTO `filmfinder`.`userXrating`(user_id,movie_id,rating,comment_id) VALUES (%s,{last_id});"
                print(sql%(rating_values))
                c.execute(sql%(rating_values))
                
                #update coresponding filmfinder_score for movies table
                sql = f""" UPDATE `filmfinder`.`movies` 
                set filmfinder_score = cust_rank('',movies.imdb_title_id) 
                where movies.imdb_title_id = {escape_string(request.form['movie_id'])};"""
                print(sql)
                c.execute(sql)
        except MySQLError as err:
            db.rollback()
            print(err)
        else:
            db.commit()
            return f"OK",200
    abort(400)

@comment_bp.route('/get_comments', methods=["GET"])
def get_comments():
    """
    Description
    -----------
    this function returns all comments for given movies
    if requesting user has logined in, blocked users' commnets will not return
    
    Parameter
    ---------
    @movie_id: which movie. It must not be empty.
    @page: the offset of rows. It must not be empty.
    @page_size: how many rows should be return. It must not be empty.
    
    Returns
    -------
    @rating_commnet:
        @user_id: who leavs the comment
        @rating: each user only has one comment which includes rating
        @comment_id: 
        @commnet: the body of the commnet

    """
    print("is_authenticated",current_user.is_authenticated)
    ks = {'movie_id',"page","page_size"}
    if  {'movie_id',"page","page_size"} == set(request.args.keys()):
        for k in {'movie_id',"page","page_size"} :
            if not request.args[k]:
                abort(400)
        try:
            sql = """
                select 
                userXrating.user_id,
                userXrating.rating,
                userXcomment.comment_id,
                userXcomment.comment,
                users.nick_name
                from filmfinder.userXrating 
                left join filmfinder.userXcomment
                on userXrating.comment_id = userXcomment.comment_id
                left join filmfinder.users
                on userXcomment.user_id = users.user_id
                %s -- where
                %s -- limit
                """
               
            where = "Where "
            # if "user_id" in request.args and request.args['user_id']:
            #     where += f"user_id = '{escape_string(request.args['user_id'])}' And"
            if request.args['movie_id']:
                where += f"userXrating.movie_id = {escape_string(request.args['movie_id'])} And"
               
            if current_user.is_authenticated:
                sub_sql = f"select blocklisted_user from `filmfinder`.`blocklist` where user_id = '{current_user.get_id()}'" 
                where += f" userXrating.user_id not in ({sub_sql}) And"
                
            size = int(escape_string(request.args['page_size']))
            if size >50:
                size = 50
            limit = f"limit {size}"
            if "page" in request.args:
                offset = (int(escape_string(request.args['page'])) -1 )* size
                limit += f" OFFSET {offset}"
            where = where[:-4]
            db = get_db(current_app)
            with db.cursor() as c:
                # get all comment 
                # print(sql%(where,limit))
                c.execute(sql%(where,limit))
                comments = c.fetchall()
                # get all response
                responses = dict()
                for com in comments:
                    response_sql = """select userXcomment.*,commentXresponse.response_to,users.nick_name
                                    from filmfinder.userXcomment 
                                    left join filmfinder.commentXresponse
                                    on userXcomment.comment_id = commentXresponse.comment_id
                                    left join filmfinder.users
                                    on userXcomment.user_id = users.user_id
                                    where ancestor_comment_id = %s
                                    and userXcomment.comment_id != %s """
                    if current_user.is_authenticated:
                        response_sql += f"and userXcomment.user_id not in (select blocklisted_user from `filmfinder`.`blocklist` where user_id = '{current_user.get_id()}')"
                    print(response_sql)
                    c.execute(response_sql,(com['comment_id'],com['comment_id']))
                    responses[com['comment_id']] = c.fetchall()
            return jsonify({'comments':comments,"responses":responses})   
        except MySQLError as err:
            db.rollback()
            print(err)
        else:
            return f"OK",200
    abort(400)