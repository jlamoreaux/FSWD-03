#!/usr/bin/python

import psycopg2


conn = psycopg2.connect("dbname=news")

cursor = conn.cursor()


# List of top 3 popular articles
def popular_articles():
    cursor.execute(
        SELECT articles.title, COUNT(log.ip)
        FROM articles
        JOIN log ON log.path
        LIKE CONCAT('%', articles.slug, '%')
        GROUP BY title
        ORDER BY COUNT DESC
        LIMIT 3;
    )


# List of authors in order of popularity
def popular_authors():
    cursor.execute(
        SELECT authors.name, COUNT(popular.ip)
        FROM authors
        JOIN(SELECT articles.title, articles.author, log.ip FROM articles
             JOIN log ON log.path LIKE CONCAT('%', articles.slug, '%'))
        AS popular
        ON authors.id=popular.author
        GROUP BY name
        ORDER BY COUNT DESC;
    )


# Day with the highest number of errors
def high_errors():
    cursor.execute(
        SELECT DATE(time) AS ForDate, COUNT(status)
        FROM log WHERE status != '200 OK'
        GROUP BY ForDate
        ORDER BY COUNT DESC
        LIMIT 1;
    )

popular_articles()
popular_authors()
high_errors()
