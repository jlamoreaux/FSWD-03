#!/usr/bin/python
import psycopg2
import sys

conn = psycopg2.connect("dbname=news")

cursor = conn.cursor()

def popular_articles()
    cursor.execute(
        SELECT articles.title, COUNT(log.ip)
        FROM articles
        JOIN log ON log.path LIKE CONCAT('%', articles.slug, '%')
        GROUP BY title ORDER BY COUNT DESC LIMIT 3;
    )
    return

def popular_authors()
    cursor.execute(

    )

def high_errors()
    cursor.execute(

    )
