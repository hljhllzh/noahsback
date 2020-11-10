# -*- coding: utf-8 -*-

from . import film_bp,GENRE
from backend import get_db, printR
from flask import abort, request, current_app,jsonify
from flask_login import current_user
from pymysql import escape_string, MySQLError
from decimal import Decimal

@film_bp.route('/get', methods=['GET'])
def get_film():
    """
    Parameters
    ----------
    @movies_id: which movie
    
    -------
    @filmfinder_score: score which calculate by our algorithm,
                       if user has logined in, tailored results will be returned.
    imdb_title_id,
    @title`,
    @original_title`,
    @date_published`,
    @genre`,
    @duration`,
    @country`,
    @language`,
    @director`,
    @writer`,
    @production_company`,
    @actors`,
    @description`,
    @avg_vote`,
    @votes`,
    @budget`,
    @usa_gross_income`,
    @worlwide_gross_income`,
    @metascore`,
    @reviews_from_users`,
    @reviews_from_critics`,
    @year`,
    image: the cover image name

    """
    try:
        if 'movie_id' in request.args:
            
            db = get_db(current_app)
            with db.cursor() as c:
                if current_user.is_authenticated:
                    sql = f"""SELECT cust_rank('{current_user.get_id()}',m.imdb_title_id) as filmfinder_score,
                    m.imdb_title_id,
                    m.`title`,
                    m.`original_title`,
                    m.`date_published`,
                    m.`genre`,
                    m.`duration`,
                    m.`country`,
                    m.`language`,
                    m.`director`,
                    m.`writer`,
                    m.`production_company`,
                    m.`actors`,
                    m.`description`,
                    m.`avg_vote`,
                    m.`votes`,
                    m.`budget`,
                    m.`usa_gross_income`,
                    m.`worlwide_gross_income`,
                    m.`metascore`,
                    m.`reviews_from_users`,
                    m.`reviews_from_critics`,
                    m.`year`,
                    m.`image` 
                    from filmfinder.movies as m 
                    where m.imdb_title_id = %s
                    """
                else:
                    sql = "SELECT movies.* from filmfinder.movies where imdb_title_id = %s"
                print(sql%(request.args['movie_id']))
                c.execute(sql,(request.args['movie_id']))  
                tmp = c.fetchone()
                tmp['filmfinder_score'] = float(tmp['filmfinder_score'])
                tmp['date_published'] = tmp['date_published'].isoformat()
                tmp['year'] = tmp['year'].isoformat()
                return jsonify(tmp) 
    except MySQLError as err:
        print(err)
    abort(400)
    
@film_bp.route('/top', methods=['GET'])
def top():
    """
    Description
    -----------
    This function returns top n films which rank by filmfinder score.
    If the user have logined in, the tailored ranking will be returned 
    
    Parameters
    ----------
    @min_date_published (optional,imdb col):  YYYY-MM-DD hh:mm:ss ', default "2019-01-01"
    @max_date_published (optional, imdb col):  YYYY-MM-DD hh:mm:ss ', optional
    @min_votes (optional,imdb col): for more acurate ranking, you set minmun votes for the film. default 2000
    @genre[](otional): send as comma separated string. e.g. in ajax "1,2,3" -> in python [1,2,3]
            returns rank for given each genre,
            if wrong genre or empyt genre is sent, it returns ranking for all genre
    @page_size (required): request as top n film, if size greater than 50, size = 50
    
    Returns 
    -------
    top N movies in each genre in json
    @filmfinder_score: score which calculate by our algorithm,
                       if user has logined in, tailored results will be returned.
    imdb_title_id,
    @title`,
    @original_title`,
    @date_published`,
    @genre`,
    @duration`,
    @country`,
    @language`,
    @director`,
    @writer`,
    @production_company`,
    @actors`,
    @description`,
    @avg_vote`,
    @votes`,
    @budget`,
    @usa_gross_income`,
    @worlwide_gross_income`,
    @metascore`,
    @reviews_from_users`,
    @reviews_from_critics`,
    @year`,
    image: the cover image name

    """
    if 'page_size' in request.args:
        try:
            select_from,where,limit = film_sql(auth=current_user.is_authenticated)
            # print(select_from,where,limit )    
            db = get_db(current_app)
            result = dict()
            with db.cursor() as c:
                if GENRE.issuperset(set(request.args.getlist("genre[]"))) and request.args.getlist("genre[]"):
                    genre = request.args.getlist("genre[]") 
                    for gen in genre:
                        tmp_where = where + f" movies.genre like '%{escape_string(gen)}%' " 
                        if current_user.is_authenticated:
                            print(select_from%(current_user.get_id(),tmp_where,limit))
                            c.execute(select_from%(current_user.get_id(),tmp_where,limit))
                        else: 
                            # print(select_from%("",tmp_where,limit))
                            c.execute(select_from%(tmp_where,limit))
                        tmp = c.fetchall()
                        tmp = format_result(tmp)
                        result[gen] = tmp
                            
                else:
                    where = where[:-4]
                    if current_user.is_authenticated:
                        # print (" is  auth")
                        # print(select_from%(current_user.get_id(),where,limit))
                        c.execute(select_from%(current_user.get_id(),where,limit))
                    else: 
                        # print(select_from%(where,limit))
                        c.execute(select_from%(where,limit))
                    tmp = c.fetchall()
                    tmp = format_result(tmp)
                    result["All"] = tmp
            return jsonify(result)
        except MySQLError as err:
            print(err)
    abort(400)

def format_result(result):
    print(len(result))
    for id in range(len(result)):
        result[id]['filmfinder_score'] = float(result[id]['filmfinder_score'])
        result[id]['date_published'] = result[id]['date_published'].isoformat()
        result[id]['year'] = result[id]['year'].isoformat()
    return result
 
def film_sql(auth=False):
    if auth:
        select_from = """
            select cust_rank('%s',m.imdb_title_id) as filmfinder_score, 
                    m.imdb_title_id,
                    m.`title`,
                    m.`original_title`,
                    m.`date_published`,
                    m.`genre`,
                    m.`duration`,
                    m.`country`,
                    m.`language`,
                    m.`director`,
                    m.`writer`,
                    m.`production_company`,
                    m.`actors`,
                    m.`description`,
                    m.`avg_vote`,
                    m.`votes`,
                    m.`budget`,
                    m.`usa_gross_income`,
                    m.`worlwide_gross_income`,
                    m.`metascore`,
                    m.`reviews_from_users`,
                    m.`reviews_from_critics`,
                    m.`year`,
                    m.`image` 
              from (
               	select movies.*
                  from filmfinder.movies
                  %s -- where
               	  order by movies.filmfinder_score desc
                  limit 500
              ) as m 
              order by filmfinder_score desc
              %s; -- limit
             """
    else:
        select_from = """select movies.* from filmfinder.movies  
                    %s -- where
                    order by filmfinder_score desc
                    %s;-- limit """
    
    where = "where "
    
    if 'min_date_published' in request.args:
        where += f" movies.date_published >= '{escape_string(request.args['min_date_published'])}' And "
    else:
        where += f" movies.date_published >= '2019-01-01' And "
        
    if 'max_date_published' in request.args:
        where += f" movies.date_published <= '{escape_string(request.args['max_date_published'])}' And "
        
    if 'min_votes' in request.args:
        where += f" movies.votes >= {escape_string(request.args['min_votes'])} And "
    else:
        
        where += f" movies.votes >= 2000 And "
        
    limit = ""
    size = int(escape_string(request.args['page_size']))
    if size >50:
        size = 50
    limit += f"limit {size}"
    if "page" in request.args:
        offset = (int(escape_string(request.args['page'])) -1 )* size
        limit +=     f" OFFSET {offset}"
     
    return select_from,where,limit
    
# @film_bp.route('/top', methods=['GET'])
# def top():
#     """
#     Description
#     -----------
#     This function returns top n films which rank by filmfinder score.
#     If the user have logined in, the tailored ranking will be returned 
    
#     Parameters
#     ----------
#     min_date_published :  YYYY-MM-DD hh:mm:ss ', default "2019-01-01"
#     max_date_published :  YYYY-MM-DD hh:mm:ss ', optional
#     min_votes: for more acurate ranking, you set minmun votes for the film (imdb vote count)
#                default 2000
#     genre: send as comma separated string. e.g. in ajax "1,2,3" -> in python [1,2,3]
#            returns rank for given each genre,
#            if wrong genre or empyt genre is sent, it returns ranking for all genre
#     page_size: request as top n film, if size greater than 50, size = 50
#     page: control offset
    
#     Returns 
#     -------
#     top N movies in each genre in json

#     """
#     try:
#         if 'page_size' in request.args:
            
            
            
#             sql,where,order,limit = film_sql() 
#             if 'genre[]' in request.args and GENRE.issuperset(set(request.args.getlist("genre[]"))) and request.args.getlist("genre[]"):
#                 genre = request.args.getlist("genre[]") 
#                 result = dict()
#                 db = get_db(current_app)
#                 with db.cursor() as c:
#                     for gen in genre:
#                         tmp_where = where + f" m.genre like '%{escape_string(gen)}%' "
                        
#                         print(sql%(current_user.get_id(),tmp_where,order,limit))
#                         c.execute(sql%(current_user.get_id(),tmp_where,order,limit))
#                         result[gen] = c. fetchall()
#             else:
#                 sql = """
#                       select cust_rank(%s,m.imdb_title_id) as cust, m.*  
#                         from (
#                         	select movies.*
#                             from filmfinder.movies
#                             where movies.votes >2000
#                             and movies.date_published > "2019-01-01"
#                         	order by movies.avg_vote desc
#                             limit 500
#                         ) as m 
#                         order by cust desc; 
#                      """
            
            
#             # print(result)
#             return jsonify(result)
#     except MySQLError as err:
#         print(err)
#     abort(400)
    
# @film_bp.route('/get', methods=['GET'])
# def get_film():
#     """
#     Parameters
#     ----------
 
#     -------
#     Returns top N movies in each genre in json

#     """
#     try:
#         if 'movie_id' in request.args:
#             sql = "SELECT cust_rank(%s,movies.imdb_title_id) as filmfinder_score,movies.* from filmfinder.movies where imdb_title_id = %s"
#             db = get_db(current_app)
#             with db.cursor() as c:
#                 # print(sql%(current_user.get_id(),request.args['movie_id']))
#                 c.execute(sql,(current_user.get_id(),request.args['movie_id']))  
#                 tmp = c.fetchone()
#                 tmp['filmfinder_score'] = float(tmp['filmfinder_score'])
#                 tmp['date_published'] = tmp['date_published'].isoformat()
#                 tmp['year'] = tmp['year'].isoformat()
#                 return jsonify(tmp) 
#     except MySQLError as err:
#         # print(err)
#         pass
#     abort(400)
    
    
# def film_sql():
#     sql = """
#       select cust_rank(%s,m.imdb_title_id) as filmfinder_score, m.*  
#         from (
#         	select movies.*
#             from filmfinder.movies
#             %s -- where
#         	%s -- order by
#             limit 500
#         ) as m 
#         order by cust desc
#         %s; -- limit
#      """
#     # sql = """SELECT 
#     #                 m.`title`,
#     #                 m.`original_title`,
#     #                 m.`date_published`,
#     #                 m.`genre`,
#     #                 m.`duration`,
#     #                 m.`country`,
#     #                 m.`language`,
#     #                 m.`director`,
#     #                 m.`writer`,
#     #                 m.`production_company`,
#     #                 m.`actors`,
#     #                 m.`description`,
#     #                 m.`avg_vote`,
#     #                 m.`votes`,
#     #                 m.`budget`,
#     #                 m.`usa_gross_income`,
#     #                 m.`worlwide_gross_income`,
#     #                 m.`metascore`,
#     #                 m.`reviews_from_users`,
#     #                 m.`reviews_from_critics`
#     #                 m.`image`
#     #                 from filmfinder.movies as m
#     #                 inner join  filmfinder.ratings as r
#     #                 on m.imdb_title_id = r.imdb_title_id
#     #                 %s -- where 
#     #                 %s -- order 
#     #                 %s -- limit 
#     #                 """
#     where = "where "
    
#     if 'min_date_published' in request.args:
#         where += f" m.date_published >= '{escape_string(request.args['min_date_published'])}' And "
#     else:
#         where += f" m.date_published >= '2019-01-01' And "
        
#     if 'max_date_published' in request.args:
#         where += f" m.date_published <= '{escape_string(request.args['max_date_published'])}' And "
        
#     if 'min_votes' in request.args:
#         where += f" m.votes >= {escape_string(request.args['min_votes'])} And "
#     else:
        
#         where += f" m.votes >= 2000 And "
         
#     """ 
#         ranking options
#         ---------------
#         `filmfinder_score`
#         `weighted_average_vote`,
#         `total_votes`,
#         `mean_vote`,
#         `median_vote`,
#         `votes_10`,
#         `votes_9`,
#         `votes_8`,
#         `votes_7`,
#         `votes_6`,
#         `votes_5`,
#         `votes_4`,
#         `votes_3`,
#         `votes_2`,
#         `votes_1`,
#         `allgenders_0age_avg_vote`,
#         `allgenders_0age_votes`,
#         `allgenders_18age_avg_vote`,
#         `allgenders_18age_votes`,
#         `allgenders_30age_avg_vote`,
#         `allgenders_30age_votes`,
#         `allgenders_45age_avg_vote`,
#         `allgenders_45age_votes`,
#         `males_allages_avg_vote`,
#         `males_allages_votes`,
#         `males_0age_avg_vote`,
#         `males_0age_votes`,
#         `males_18age_avg_vote`,
#         `males_18age_votes`,
#         `males_30age_avg_vote`,
#         `males_30age_votes`,
#         `males_45age_avg_vote`,
#         `males_45age_votes`,
#         `females_allages_avg_vote`,
#         `females_allages_votes`,
#         `females_0age_avg_vote`,
#         `females_0age_votes`,
#         `females_18age_avg_vote`,
#         `females_18age_votes`,
#         `females_30age_avg_vote`,
#         `females_30age_votes`,
#         `females_45age_avg_vote`,
#         `females_45age_votes`,
#         `top1000_voters_rating`,
#         `top1000_voters_votes`,
#         `us_voters_rating`,
#         `us_voters_votes`,
#         `non_us_voters_rating`,
#         `non_us_voters_votes`
#     """
#     order = ""
#     if 'rank_by' in request.args:
#         order += f"Order by r.{escape_string(request.args['rank_by'])} DESC "

#     limit = ""
#     if "page_size" in request.args:
#         size = int(escape_string(request.args['page_size']))
#         if size >50 or "cust_rank" == request.args['rank_by']:
#             size = 50
#         limit += f"limit {size}"
#         if "page" in request.args:
#             offset = (int(escape_string(request.args['page'])) -1 )* size
#             limit += f" OFFSET {offset}"
#     return sql,where,order,limit
    