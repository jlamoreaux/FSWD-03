# Log Analysis

Log Analysis is a Python script that queries a PostgreSQL database using the psycopg2 library.
The database is a mock database for a fictional news website. The script accesses three
different tables to return the data listed below under **Running the Program**.

## Requirements
- Python 3.5.2
- PostgreSQL 9.5.7
- psycopg 2.7.3

## Usage

You must have the newsdata.sql file imported to PostgreSQL for this program to work.

## Running the Program

To run the program using a command prompt, navigate to the folder holding this file
and execute the following command:
`python3 report.py`

The following results will be returned from the database:
- Most Popular Articles
- Popularity of Authors
- Days With HTTP Error Rates Over 1%
