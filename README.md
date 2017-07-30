# Log Analysis

Log Analysis is a Python script that queries a PostgreSQL database using the psycopg2 library.
The database is a mock database for a fictional news website.
The script accesses three different tables to return the data listed below under **Running the Program**.

## Requirements
- Python 3.5.2
- PostgreSQL 9.5.7
- psycopg 2.7.3

## Setup

The file [newsdata.sql](https://github.com/jlamoreaux/FSWD-03/blob/master/newsdata.zip) can be found in this repository and must be imported to PostgreSQl
for this program to work.
Navigate, via your computer's shell, to the folder where _newsdata.sql_ has been downloaded and execute the following command:
`psql -d news -f newsdata.sql`
It may take a minute or two to complete the import.
Once the database has been loaded, you need to create a view, `errors`, for the python script to access.
You can do so by executing the following:

`$ psql news` (Opens PostgreSQL and connects to the database)

`=>CREATE VIEW "errors" AS
SELECT DATE(time) AS date,
COUNT(*) FILTER (WHERE status = '404 NOT FOUND') AS fail, 
COUNT(*) AS total
FROM log GROUP BY date;`
(Creates the required view)

`\q` (Exits PSQL)

You can now run the program.


## Running the Program

To run the program using a command prompt, navigate to the folder containing _report.py_ and execute the following command:
`python3 report.py`

The following results will be returned from the database:
- Most Popular Articles
- Popularity of Authors
- Days With HTTP Error Rates Over 1%
