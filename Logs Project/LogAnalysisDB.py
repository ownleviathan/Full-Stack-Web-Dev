# import pycodestyle
import psycopg2, bleach

DBName = "news"


def get_three_popular_articles():
    db = psycopg2.connect(database=DBName)
    c = db.cursor()
    query = """
        SELECT articles.title, count(*)
        FROM   log, articles
        WHERE  log.path = '/article/' || articles.slug
        GROUP BY articles.title
        ORDER BY count(*) DESC
        LIMIT 3;
    """
    c.execute(query)
    popularThree = c.fetchall()
    db.close()
    return popularThree

def get_most_popular_author_alltime():
    db = psycopg2.connect(database=DBName)
    c = db.cursor()
    query = """
        SELECT authors.name,count(*)
            FROM   log,articles,authors
            WHERE  log.path = '/article/' || articles.slug
            AND articles.author = authors.id
            GROUP BY authors.name
            ORDER BY count(*) DESC;
    """
    c.execute(query)
    popularAuthor = c.fetchall()
    db.close()
    return popularAuthor

def request_lead_to_errors():
    db = psycopg2.connect(database=DBName)
    c = db.cursor()
    query = """
        CREATE or REPLACE VIEW log_status as
        SELECT Date,Total,Error, (Error::float*100)/Total::float as Percent FROM
        (SELECT time::timestamp::date as Date, count(status) as Total, sum(case when status = '404 NOT FOUND' then 1 else 0 end) as Error FROM log
        GROUP BY time::timestamp::date) as result
        WHERE (Error::float*100)/Total::float > 1.0 ORDER BY Percent desc;
    """
    c.execute(query)

    query2 = """
        SELECT date, total, error, percent 
        FROM log_status;"""

    c.execute(query2)    
    leadErrors = c.fetchall()
    db.close()
    return leadErrors