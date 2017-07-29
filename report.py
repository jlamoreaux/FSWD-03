#!/usr/bin/python3

import psycopg2


def connect(db_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format("news"))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print("Unable to connect to database")
        sys.exit(1)


def get_query_results(query):
    db, c = connect()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def print_top_articles():
    output = get_query_results(
        '''SELECT articles.title, COUNT(log.ip)
        FROM articles
        JOIN log ON log.path
        LIKE CONCAT('%', articles.slug, '%')
        GROUP BY title
        ORDER BY COUNT DESC
        LIMIT 3;'''
    )
    print("\nMost Popular Articles: \n")
    for x in output:
        print(str(x[0]) + " -- " + str(x[1]) + " views")


def print_top_authors():
    output = get_query_results(
        '''SELECT authors.name, COUNT(popular.ip)
        FROM authors
        JOIN(SELECT articles.title, articles.author, log.ip FROM articles
             JOIN log ON log.path LIKE CONCAT('%', articles.slug, '%'))
        AS popular
        ON authors.id=popular.author
        GROUP BY name
        ORDER BY COUNT DESC;'''
    )
    print("\nPopularity of Authors: \n")
    for x in output:
        print(str(x[0]) + " -- " + str(x[1]) + " views")


def print_top_error_days():
    output = get_query_results(
        '''SELECT DATE(time) AS ForDate,
           ROUND(COUNT(status)*100/SUM(COUNT(status)) OVER(), 2) AS Percentage
        FROM log WHERE status != '200 OK'
        GROUP BY ForDate
        ORDER BY Percentage DESC
        LIMIT 1;'''
    )
    for x in output:
        print("\nDay With Highest Error Rate:\n\n" + str(x[0]) +
              " -- " + str(x[1]) + "%")


if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_top_error_days()
