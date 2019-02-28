#!/usr/bin/env python3
three_popular_articles = """
        SELECT articles.title, count(*)
        FROM   log, articles
        WHERE  log.path = '/article/' || articles.slug
        GROUP BY articles.title
        ORDER BY count(*) DESC
        LIMIT 3;
    """

most_popular_authors = """
        SELECT authors.name,count(*)
            FROM   log,articles,authors
            WHERE  log.path = '/article/' || articles.slug
            AND articles.author = authors.id
            GROUP BY authors.name
            ORDER BY count(*) DESC;
    """

view_lead_to_errors = """
        CREATE or REPLACE VIEW log_status as
        SELECT Date,Total,Error, (Error::float*100)/Total::float
        AS Percent FROM
        (SELECT time::timestamp::date as Date, count(status) as Total,
        sum(case when status = '404 NOT FOUND' then 1 else 0 end)
        AS Error FROM log
        GROUP BY time::timestamp::date) as result
        WHERE (Error::float*100)/Total::float > 1.0 ORDER BY Percent desc;
    """

lead_to_erros = """
        SELECT date, total, error, percent
        FROM log_status;
    """
