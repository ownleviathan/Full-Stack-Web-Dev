import psycopg2
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
        LIMIT 3; """
    
    results = run_query_onDB(query)

    print('\n*****************************************************')
    print('What are the most popular three articles of all time?')
    print('*****************************************************\n')
    print('Article                           #of Views')
    print('-------------------------------------------')
    for var in results:        
        print(str(var[0]) + '  ' +  str(var[1]))

def get_most_popular_author_alltime():
    query = """
        SELECT authors.name,count(*)
        FROM   log,articles,authors
        WHERE  log.path = '/article/' || articles.slug
        AND articles.author = authors.id
        GROUP BY authors.name
        ORDER BY count(*) DESC; """
    results = run_query_onDB(query)
    
    print('\n*****************************************************')
    print('Who are the most popular article authors of all time?')
    print('*****************************************************\n')
    print('Author                           #of Views')
    print('-------------------------------------------')
    for var in results:        
        print(str(var[0]) + '  \t\t' +  str(var[1]))

def request_lead_to_errors():
    query = """
        CREATE or REPLACE VIEW log_status as
        SELECT Date,Total,Error, (Error::float*100)/Total::float as Percent FROM
        (SELECT time::timestamp::date as Date, count(status) as Total, sum(case when status = '404 NOT FOUND' then 1 else 0 end) as Error FROM log
        GROUP BY time::timestamp::date) as result
        WHERE (Error::float*100)/Total::float > 1.0 ORDER BY Percent desc;"""
    
    run_query_notReturn(query)

    query2 = """
        SELECT date, total, error, percent 
        FROM log_status;"""

    results = run_query_onDB(query2)

    print('\n*******************************************************')
    print('On which days did more than 1\% of requests lead to errors?')
    print('*******************************************************\n')
    print('Date\t\t\tTotal\t\tError\t\tPercent')
    print('-------------------------------------------')
    for var in results:        
        print(str(var[0]) + '\t\t' +  str(var[1]) + '\t\t' +  str(var[2]) + '\t\t' +  str(var[3]))


get_three_popular_articles()
get_most_popular_author_alltime()
request_lead_to_errors()