import pandas as pd 
import numpy as np

# ============================================================================ #
#                    Reading and Writing Data in Text Format                   #
# ============================================================================ #

# text and binary data loading functions
# read_csv - delimited data from a file, uril, comma is default delimiter
# read_fwf - fixed width column format
# read_clipboard - reads data from the clipboard
# read_excel - xls or xlsx
# read_hdf - read hdf5 written by pandas
# read_html - all tables in a html doc
# read_json - json
# read_feather - feather binary file
# read_orc - apache orc binary file
# read_parquet - apache parquet binary file
# read_pickle - read object stored by pandas using pickle format
# read_sas - SAS dataset
# read_spss - spss data file
# read_sql - read the results of SQL query
# read_sql_table - read the whole sql table
# read_stata - dta files
# read_xml - xml

# Basic file
df = pd.read_csv("examples/ex1.csv")
df 

# No header row / colnames
# !cat examples/ex2.csv 
pd.read_csv("examples/ex2.csv", header=None)

# can assign colnames 
pd.read_csv("examples/ex2.csv", names = ["a", "b", "c", "d", "message"])

# can assign col as index
names = ["a", "b", "c", "d", "message"]
pd.read_csv("examples/ex2.csv", names = names, index_col = "message")

# if you want a hierarchical index, you can pass a list of cols
# !cat examples/csv_mindex.csv

parsed = pd.read_csv("examples/csv_mindex.csv", 
                     index_col = ["key1", "key2"])
parsed 

# in some cases, a table might not have a fixed delimiter
# !cat examples/ex3.txt
# the fields are separated by a variable amount of whitespace
# you can pass regex as a delimiter \s - any white space character + - one or more of the thing before it
result = pd.read_csv("examples/ex3.txt", sep = r"\s+")
result

# file parsing have many additional arguments
# e.g. can skip rows
# !cat examples/ex4.csv
pd.read_csv("examples/ex4.csv", skiprows = [0, 2, 3])

# dealing with missing data
# !cat examples/ex5.csv

result = pd.read_csv("examples/ex5.csv")
result  
pd.isna(result)

# na_values accepts strings to add to the detault list of strings recognized as missing
result = pd.read_csv("examples/ex5.csv", na_values = ["NULL"])
result 

# can disable default NA representations
result2 = pd.read_csv("examples/ex5.csv", keep_default_na = False)
result2
result2.isna()

result3 = pd.read_csv("examples/ex5.csv",
                      keep_default_na = False,
                      na_values = "NA")
result3 
 
# can specify what should be na by col
sentinels = {"message": ["foo", "NA"], "something":["two"]}
pd.read_csv("examples/ex5.csv", 
            keep_default_na = False,
            na_values = sentinels)

# read_csv arguments
# path - string of the file / url
# sep / delimiter - character sequence or regex to split fields in each row
# header - row number to use for colnames
# index_col - col number(s) to use as the row index
# names - list of col names for result
# skip rows - give a list of rows to ignore
# na_values - sequence of values to replace with NA
# keep_default_na - whether to use default NA value list
# comment - some text files might have comments so you can indicate the character it begins with
# parse_dates - attempt to parse datetime - false by default
# keep_date_col - if joining columns to parse date, keep the joined cols - false by default
# converters - dictionary containing col number / name mapping to functions {"foo": f} would apply function f to all values in the foo col
# dayfirst - when parsing ambiguous date, do D/M/Y - false by default
# date_format - function to use to parse dates
# nrows - number of rows to read from the beginning of the file
# iterator - return a textfilereader object for reading the file piecemeal
# chunksize - for iteration, size of file chunks
# skip_footer - number of lines to ignore at the end of file
# verbose - print various parsing info
# encoding - text encoding
# squeeze - if the parsed data contains only one col, return a series
# thousands, separator for thousands (",") - default is none
# decimal - decimal separator in numbers - default is "."
# engine - "c", "python", "pyarrow"
# c is default, use this in most cases, 
# use python just for complex parsing, regex separators
# pyarrow for very large files - supports multithreading

# ----------------------- Reading Text Files in Pieces ----------------------- #
pd.options.display.max_rows = 10
result = pd.read_csv("examples/ex6.csv")
result 

# reading just 5 rows
pd.read_csv("examples/ex6.csv", nrows = 5)

# to read a file in pieces, use chunksize argument
chunker = pd.read_csv("examples/ex6.csv", chunksize = 1_000)
type(chunker)
# returns a TextFileReader object that lets us iterate over parts of the file

# e.g. aggregating the value counts of the key column
chunker = pd.read_csv("examples/ex6.csv", chunksize = 1_000)
tot = pd.Series([], dtype = "int64")

for piece in chunker:
    tot = tot.add(piece["key"].value_counts(), fill_value = 0)

tot = tot.sort_values(ascending = False) 
tot[:10]

# ------------------------ Writing Data to Text Format ----------------------- #
data = pd.read_csv("examples/ex5.csv")
data 

# convert dfs to csv with to_csv

data.to_csv("examples/out.csv")

# other delimiters can be used
data.to_csv("examples/out.tsv", sep = "\t")

# NAs are converted to empty strings in to_csv, can be explicit on what you want NAs to be
data.to_csv("examples/out2.csv", na_rep = "NULL")

# can remove row and col labels 
data.to_csv("examples/out3.csv", header = False, index = False)

# can also select which cols to export
data.to_csv("examples/out4.csv", index = False, columns = ["a", "b", "c"])

# ------------------- Working with Other Delimited Formats ------------------- #
# !cat examples/ex7.csv

# for any file with a single character delimiter, you can use csv package
import csv 
f = open("examples/ex7.csv")
reader = csv.reader(f)

# iterating through the reader yields lists of values with any quote characters removed
for line in reader:
    print(line)
f.close()


# first we read the file into a list of lines
with open("examples/ex7.csv") as f:
    lines = list(csv.reader(f))

# then we split the lines into header and data lines
header, values = lines[0], lines[1:]

data_dict = {h:v for h, v in zip(header, zip(*values))}
data_dict 

# to define a new format with a different delimiter, string quoting convention or line terminator, we use a simple subclass of csv.Dialect
class my_dialect(csv.Dialect):
    lineterminator = "\n"
    delimiter = ";"
    quotechar = '"'
    quoting = csv.QUOTE_MINIMAL 

# we could also give individual csv dialect parameters as keywords to csv.reader
reader = csv.reader(f, delimiter = "|")

# csv dialect options
# delimiter - one char string to separate fields
# lineterminator - line terminator for writing 
# quotechar - quote character for fields with special chars
# quoting - QUOTE_ALL - quote all fields; QUOTE_MINIMAL - only fields with quotechar; QUOTE_NONNUMERIC and QUOTE_NONE
# skipinitialspace - ignore whitespace after each delimiter
# doublequote - how to handle quoting character inside, 
# escape character - string to escape the delimiter if quoting is csv.QUOTE_NONE

# --------------------------------- JSON Data -------------------------------- #
# standard format for sending data by HTTP request 
# more free form data format

obj = """
{"name": "Wes",
 "cities_lived": ["Akron", "Nashville", "New York", "San Francisco"],
 "pet": null,
 "siblings": [{"name": "Scott", "age": 34, "hobbies": ["guitars", "soccer"]},
              {"name": "Katie", "age": 42, "hobbies": ["diving", "art"]}]
}
"""

import json 
# very similar to python except null and other small differences
# basic types - objects (dictionaries), arrays (lists), strings, numbers, booleans, nulls

result = json.loads(obj)  # reads json
result 

asjson = json.dumps(result) # converts python object -> json
asjson

siblings = pd.DataFrame(result["siblings"], columns = ["name", "age"])
siblings 
# you can pass a list of dictionaries to the DataFrame() and select a subset of cols
# alternatively, you can use read_json that automatically converts json to DataFrame
# !cat examples/example.json

data = pd.read_json("examples/example.json")
data 

# can export to json using to_json()

# ------------------------ XML and HTML: Web Scraping ------------------------ #
# pd has a read_hyml which uses lxml, Beautiful Soup, html5lib to automatically parse tables out of HTML files as dfs

# read_html yields a list of DataFrames
tables = pd.read_html("examples/fdic_failed_bank_list.html")
tables
len(tables) # number of dfs

failures = tables[0]
failures.head()

close_timestamps = pd.to_datetime(failures["Closing Date"])
close_timestamps.dt.year.value_counts()

## Parsing XML with lxml.objectify
from lxml import objectify 
path = "datasets/mta_perf/Performance_MNR.xml"
with open(path) as f:
    parsed = objectify.parse(f)

# we parse the file and get a reference ot the root node with getroot
root = parsed.getroot()

# root.INDICATOR returns a generator yielding each INDICATOR XML element
# for each record, we can populate a dictionary of tag names to data values
data = []
skip_fields = ["PARENT_SEQ", "INDICATOR_SEQ", "DESIRED_CHANGE", "DECIMAL_PLACES"]

for elt in root.INDICATOR:
    el_data = {}
    for child in elt.getchildren():
        if child.tag in skip_fields:
            continue
        el_data[child.tag] = child.pyval 
    data.append(el_data)

# then convert this list of dictionaries into a df
perf = pd.DataFrame(data)
perf.head()

# pd.read_xml does all this in one expression
perf2 = pd.read_xml(path)
perf2

# ============================================================================ #
#                              Binary Data Formats                             #
# ============================================================================ #

fec = pd.read_parquet("datasets/fec/fec.parquet")

# ---------------------------- Reading Excel Files --------------------------- #
xlsx = pd.ExcelFile("examples/ex1.xlsx")
xlsx.sheet_names 
xlsx.parse(sheet_name = "Sheet1")

# we can use index_col arg
xlsx.parse(sheet_name = "Sheet1", index_col = 0)

# if you are reading multiple sheets in a file, then it is faster to use pd.ExcelFile
# otherwise, you can just use read_excel
frame = pd.read_excel("examples/ex1.xlsx", sheet_name = "Sheet1")
frame 

# to write pandas to excel format, you need to create an excel writer
writer = pd.ExcelWriter("examples/ex2.xlsx")
frame.to_excel(writer)
writer.close()

frame.to_excel("examples/ex2.xlsx")

# -------------------------------- HDF5 Format ------------------------------- #
# intended for storing large quantities of scientific array data
# each can store multiple datasets and supporting metadata
# HDF5 supports on the fly compression
# HDF5 can be a good choice for working with datasets that don't fit into memory 
# as you can efficiently read and write small sections of much larger arrays

frame = pd.DataFrame({"a": np.random.standard_normal(100)})
store = pd.HDFStore("examples/mydata.h5")
store["obj1"] = frame 
store["obj1_col"] = frame["a"]
store 

store["obj1"]

# HDFStore supports two storage schemas, fixed and table
# the latter is slower but supports query operations using special syntax
store.put("obj2", frame, format = "table")
store.select("obj2", where = ["index >= 10 and index <= 15"])
store.close()

# put is an explicit version fo store["obj2"] = frame
# but let's us set other options

# pd.read_hdf gives a shortcut to these
frame.to_hdf("examples/mydata.h5", key="obj3", format = "table")
pd.read_hdf("examples/mydata.h5", key = "obj3", where = ["index < 5"])


# ============================================================================ #
#                           Interacting with Web APIs                          #
# ============================================================================ #

import requests 
url = "https://api.github.com/repos/pandas-dev/pandas/issues"
resp = requests.get(url) # actual request
resp.raise_for_status() # checking for http errors
data = resp.json() # converting request to data
data[0]["title"]

# each element in data is a dictionary 
# we can then pass them into pd.DataFrame
issues = pd.DataFrame(data, columns = ["number", "title", "labels", "state"])
issues 

# ============================================================================ #
#                          Interacting with Databases                          #
# ============================================================================ #


# ------------------------ Creating a DuckDB database ------------------------ #

import duckdb 

# with connect() if you provide a filename, it creates a database
con = duckdb.connect("mydata.duckdb")

# without an argument, you get an in-memory database that disappears when the process ends
con = duckdb.connect()

# create a table
query = """
    CREATE TABLE test (
        city VARCHAR,
        state VARCHAR,
        value DOUBLE, 
        count INTEGER
    )
"""
con.execute(query)
# this table contains four columns

## Inserting data 

# suppose we have some python data 
data = [
    ("Atlanta", "Georgia", 1.25, 6),
    ("Tallahassee", "Florida", 2.60, 3),
    ("Sacramento", "California", 1.70, 5),
]

# we can insert all of the rows using executemany()

con.executemany(
    "INSERT INTO test VALUES (?, ?, ?, ?)",
    data
)
# the ? are parameter placeholders

## Running a SQL query
con.execute("SELECT * FROM test")

# typically we would fetch rows
rows = con.execute("SELECT * FROM test").fetchall()
rows # list of sets

# the better way is to query directly into pd DataFrame
df = con.execute("""
    SELECT * 
    FROM test
""").df() # .df() converts the query directly into a df.DataFrame
df 

## SQL can filter fast
df = con.execute("""
    SELECT city, state, value
    FROM test 
    WHERE value > 1.5
    ORDER BY value DESC
""").df()
df 

## DuckDB can query data frames directly
cities = pd.DataFrame({
    "city": ["Atlanta", "Tallahassee", "Sacramento"],
    "state": ["Georgia", "Florida", "California"],
    "value": [1.25, 2.60, 1.70],
    "count": [6, 3, 5],
})

result = duckdb.sql("""
    SELECT city, state, value
    FROM cities
    WHERE value > 1.5
""")
result 

result = duckdb.sql("""
    SELECT
        state,
        AVG(value) AS avg_value,
        SUM(count) AS total_count
    FROM cities
    GROUP BY states
""").df() 

## Querying files directly

# CSV
duckdb.sql("""
    SELECT * 
    FROM 'data.csv'
    WHERE value > 100
""").df() 

# Parquet
duckdb.sql("""
    SELECT * 
    FROM 'data.parquet'
    WHERE value > 100
""").df()

## Creating a DuckDB table from pandas

# making the data frame to become a permanent table in the database
con.execute("""
    CREATE TABLE cities AS
    SELECT * FROM cities
""")

# you can then query it later
con.execute("""
    SELECT *
    FROM cities
""")

# cheat sheet 
# connect to persistent database
con = duckdb.connect("data.duckdb")

# run SQL
con.execute("SELECT * FROM sales")

# SQL → pandas
df = con.execute("SELECT * FROM sales").df()

# pandas → SQL → pandas
result = duckdb.sql("""
    SELECT *
    FROM df
    WHERE amount > 100
""").df()

# query Parquet directly
df = duckdb.sql("""
    SELECT *
    FROM 'sales.parquet'
""").df()

# query CSV directly
df = duckdb.sql("""
    SELECT *
    FROM 'sales.csv'
""").df()