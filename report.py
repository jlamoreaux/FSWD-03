#!/usr/bin/python3

import psycopg2


def connect(db_name="news"):
    """Creates and returns a connection to specified database,
    as well as a cursor for the database.

    Args:
        db_name: (optional string) the name of the databse to connect to.
                 Set to 'news' by default.
    Returns:
        db: a connection to the database.
        c: a cursor for the database."""

    try:
        db = psycopg2.connect("dbname={}".format("news"))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print("Unable to connect to database")
        sys.exit(1)


def get_query_results(query):
    """Connects to database, executes query, fetches results and closes
    connection to database.

    Args:
        query: a string written in SQL to access information in the
        database

    Returns:
        results: a list of tuples containing the fetched information
        from the database."""

    db, c = connect()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def print_top_articles():
    """Prints the top 3 articles from the news table."""

    output = get_query_results(
        '''SELECT articles.title, COUNT(path) AS views
        FROM articles
        JOIN log
        ON log.path=CONCAT('/article/', articles.slug)
        GROUP BY title
        ORDER BY views DESC
        LIMIT 3;'''
    )
    print("\nMost Popular Articles: \n")
    for x in output:
        print(str(x[0]) + " -- " + str(x[1]) + " views")


def print_top_authors():
    """Prints a sorted list of the names of the authors in order of
    popularity and their total number of views."""

    output = get_query_results(
        '''SELECT authors.name, COUNT(*) AS views
        FROM authors
        JOIN(SELECT articles.title, articles.author FROM articles
             JOIN log ON log.path LIKE CONCAT('/article/', articles.slug))
        AS popular
        ON authors.id=popular.author
        GROUP BY name
        ORDER BY views DESC;'''
    )
    print("\nPopularity of Authors: \n")
    for x in output:
        print(str(x[0]) + " -- " + str(x[1]) + " views")


def print_top_error_days():
    """Prints a sorted list of the days where more than 1 percent of HTTP
    requests lead to errors."""

    output = get_query_results(
        '''SELECT DATE(time) AS ForDate,
           ROUND(COUNT(status)*100/SUM(COUNT(status)) OVER(), 2) AS
           Percentage
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
