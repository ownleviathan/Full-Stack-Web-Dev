#!/usr/bin/env python3
import psycopg2
from queries import three_popular_articles, most_popular_authors, \
                    view_lead_to_errors, lead_to_erros
from decimal import Decimal
from datetime import date

DBNAME = "news"


def run_query_onDB(query):
    """Create the connection to database and return the resulsets."""
    db = psycopg2.connect('dbname=' + DBNAME)
    c = db.cursor()
    c.execute(query)
    db.commit()
    rows = c.fetchall()
    db.close()
    return rows


def run_query_notReturn(query):
    """Create the connection to database and only execute the query,
    not return """
    db = psycopg2.connect('dbname=' + DBNAME)
    c = db.cursor()
    c.execute(query)
    db.commit()
    db.close()


def get_three_popular_articles():
    query = three_popular_articles

    results = run_query_onDB(query)

    print('\n*****************************************************')
    print('What are the most popular three articles of all time?')
    print('*****************************************************\n')
    print('Article                           #of Views')
    print('-------------------------------------------')
    for var in results:
        print(str(var[0]) + '  ' + str(var[1]))


def get_most_popular_author_alltime():
    query = most_popular_authors
    results = run_query_onDB(query)

    print('\n*****************************************************')
    print('Who are the most popular article authors of all time?')
    print('*****************************************************\n')
    print('Author                           #of Views')
    print('-------------------------------------------')
    for var in results:
        print(str(var[0]) + '  \t\t' + str(var[1]))


def request_lead_to_errors():
    query = view_lead_to_errors

    run_query_notReturn(query)

    query2 = lead_to_erros

    results = run_query_onDB(query2)

    print('\n*******************************************************')
    print('On which days did more than 1\% of requests lead to errors?')
    print('*******************************************************\n')
    print('Date\t\t\tTotal\t\tError\t\tPercent')
    print('-------------------------------------------')

    for var in results:
        date_value = var[0].strftime("%B %d, %Y")
        error = var[2]
        percent = round(float(var[3]), 2)
        print(date_value + '\t\t' + str(var[1]) + '\t\t' + str(error) +
              '\t\t' + str(percent) + '%')


def main():
    """Generate the report."""
    get_three_popular_articles()
    get_most_popular_author_alltime()
    request_lead_to_errors()


if __name__ == "__main__":
    main()
