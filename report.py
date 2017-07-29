#!/usr/bin/python3

import psycopg2


def connect(db_name="news"):
    try:
        db = psycopg2.connect("dbname=news".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print "Unable to connect to database"
        sys.exit(1)

db, c = connect()


def get_query_results(query):
    connect()
    c.execute(query)
    results = cursor.fetchall()
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
    print("\n Most Popular Articles: \n")
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
    print("\n Popularity of Authors: \n")
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
        print("\n Most Errors In a Single Day: \n \n" + str(x[0]) +
              " -- " + str(x[1]) + " errors")


if __name__ = '__main__':
    print_top_articles()
    print_top_authors()
    print_top_error_days()

# List of top 3 popular articles
#def popular_articles():
#    cursor.execute(
#        '''SELECT articles.title, COUNT(log.ip)
#        FROM articles
#        JOIN log ON log.path
#        LIKE CONCAT('%', articles.slug, '%')
#        GROUP BY title
#        ORDER BY COUNT DESC
#        LIMIT 3;'''
#    )
#    objective1 = cursor.fetchall()
#    print("\n Most Popular Articles: \n")
#    for x in objective1:
#        print(str(x[0]) + " -- " + str(x[1]) + " views")
#    return objective1


# List of authors in order of popularity
#def popular_authors():
#    cursor.execute(
#        '''SELECT authors.name, COUNT(popular.ip)
#        FROM authors
#        JOIN(SELECT articles.title, articles.author, log.ip FROM articles
#             JOIN log ON log.path LIKE CONCAT('%', articles.slug, '%'))
#        AS popular
#        ON authors.id=popular.author
#        GROUP BY name
#        ORDER BY COUNT DESC;'''
#    )
#    objective2 = cursor.fetchall()
#    print("\n Popularity of Authors: \n")
#    for x in objective2:
#        print(str(x[0]) + " -- " + str(x[1]) + " views")
#    return objective2


# Day with the highest number of errors
#def high_errors():
#    cursor.execute(
#        '''SELECT DATE(time) AS ForDate, COUNT(status)
#        FROM log WHERE status != '200 OK'
#        GROUP BY ForDate
#        ORDER BY COUNT DESC
#        LIMIT 1;'''
#    )
#    objective3 = cursor.fetchall()
#    for x in objective3:
#        print("\n Most Errors In a Single Day: \n \n" + str(x[0]) +
#              " -- " + str(x[1]) + " errors")
#    return objective3

#popular_articles()
#popular_authors()
#high_errors()
