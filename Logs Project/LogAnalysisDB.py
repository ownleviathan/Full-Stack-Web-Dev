#!/usr/bin/env python3
import psycopg2
import bleach
from queries import three_popular_articles, most_popular_authors, \
                    view_lead_to_errors, lead_to_erros

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
    popularThree = run_query_onDB(query)
    return popularThree


def get_most_popular_author_alltime():

    query = most_popular_authors
    popularAuthor = run_query_onDB(query)
    return popularAuthor


def request_lead_to_errors():
    query = view_lead_to_errors
    run_query_notReturn(query)

    query2 = lead_to_erros

    leadErrors = run_query_onDB(query2)
    return leadErrors
