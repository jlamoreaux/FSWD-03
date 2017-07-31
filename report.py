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
    for title, views in output:
        print("\"{}\" -- {} views".format(title, views))


def print_top_authors():
    """Prints a sorted list of the names of the authors in order of
    popularity and their total number of views."""

    output = get_query_results(
        '''SELECT authors.name, COUNT(*) AS views
        FROM authors
        JOIN(SELECT articles.title, articles.author FROM articles
             JOIN log ON log.path=CONCAT('/article/', articles.slug))
        AS popular
        ON authors.id=popular.author
        GROUP BY name
        ORDER BY views DESC;'''
    )
    print("\nPopularity of Authors: \n")
    for author, views in output:
        print("\"{}\" -- {} views".format(author, views))


def print_top_error_days():
    """Prints a sorted list of the days where more than 1 percent of HTTP
    requests lead to errors."""

    output = get_query_results(
        '''SELECT date, ROUND(fail*100.0/total, 2) AS percentage
        FROM errors WHERE (fail*100.0/total) > 1
        ORDER BY percentage DESC;'''
    )
    print("\nDays With HTTP Error Rates Over 1%: \n")
    for date, rate in output:
        print("\"{}\" -- {}%".format(date, rate))


if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_top_error_days()
