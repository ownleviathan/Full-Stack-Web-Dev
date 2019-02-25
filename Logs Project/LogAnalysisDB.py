# import pycodestyle
import psycopg2, bleach

DBNAME = "news"

def run_query_onDB(query):
    """Create the connection to database and return the resulsets."""
    db = psycopg2.connect('dbname=' + DBNAME)
    c = db.cursor()
    c.execute(query)
    rows = c.fetchall()
    db.close()
    return rows

def run_query_notReturn(query):
    """Create the connection to database and only execute the query, not return """
    db = psycopg2.connect('dbname=' + DBNAME)
    c = db.cursor()
    c.execute(query)
    db.close()

def get_three_popular_articles():

    query = """
        SELECT articles.title, count(*)
        FROM   log, articles
        WHERE  log.path = '/article/' || articles.slug
        GROUP BY articles.title
        ORDER BY count(*) DESC
        LIMIT 3;
    """
    popularThree = run_query_onDB(query)
    return popularThree

def get_most_popular_author_alltime():

    query = """
        SELECT authors.name,count(*)
            FROM   log,articles,authors
            WHERE  log.path = '/article/' || articles.slug
            AND articles.author = authors.id
            GROUP BY authors.name
            ORDER BY count(*) DESC;
    """
    popularAuthor = run_query_onDB(query)
    return popularAuthor

def request_lead_to_errors():
    query = """
        CREATE or REPLACE VIEW log_status as
        SELECT Date,Total,Error, (Error::float*100)/Total::float as Percent FROM
        (SELECT time::timestamp::date as Date, count(status) as Total, sum(case when status = '404 NOT FOUND' then 1 else 0 end) as Error FROM log
        GROUP BY time::timestamp::date) as result
        WHERE (Error::float*100)/Total::float > 1.0 ORDER BY Percent desc;
    """
    run_query_notReturn(query)

    query2 = """
        SELECT date, total, error, percent 
        FROM log_status;"""
  
    leadErrors = run_query_onDB(query2)
    return leadErrors