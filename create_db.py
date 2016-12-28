#!/usr/bin/env python

import psycopg2
from sys import exit

# Connect to the database.
try:
    # Change 'xbaremenos' to your specific username and database name.
    conn = psycopg2.connect("dbname = 'xbaremenos' user = 'xbaremenos'")
except:
    print('Could not connect to DB... exiting...')
    exit(1)


# Create a cursor.
cur = conn.cursor()

# Create table books.
cur.execute("""CREATE TABLE books 
                (
                    title varchar(100), 
                    isbn varchar(13) PRIMARY KEY,
                    year integer,
                    pages integer
                ) 
                """) 

# Create table authors.
cur.execute("""CREATE TABLE authors
                (
                    id serial PRIMARY KEY,
                    name varchar(50),
                    origin varchar(50),
                    born varchar(20)
                ) 
                 """)

# Create table users.
cur.execute("""CREATE TABLE users
                (
                    id serial PRIMARY KEY,
                    kind varchar(50),
                    username varchar(25),
                    password varchar(25),
                    email varchar(30)
                ) 
                 """)

# Create table list.
cur.execute("""CREATE TABLE lists 
                (
                    name varchar(75),
                    kind varchar(25),
                    date varchar(25),
                    PRIMARY KEY (name, date)
                ) 
                 """)

# Create table publishers.
cur.execute("""CREATE TABLE publishers 
                (
                    name varchar(75) PRIMARY KEY,
                    location varchar(50),
                    established varchar(25)
                ) 
                 """)

# Create table suggestions.
cur.execute("""CREATE TABLE suggestions 
                (
                    title varchar(75),
                    date varchar(25) PRIMARY KEY
                ) 
                 """)

# Create table categories.
cur.execute("""CREATE TABLE categories 
                (
                    category varchar(75) PRIMARY KEY,
                    traffic integer 
                ) 
                 """)

# Create table published.
cur.execute("""CREATE TABLE published 
                (
                    isbn varchar(13),
                    publisher_name varchar(75),
                    published_id integer
                ) 
                 """)

# Create table in_suggestion.
cur.execute("""CREATE TABLE in_suggestion
                (
                    date varchar(25),
                    isbn varchar(13),
                    num_items integer
                ) 
                 """)

# Create table rates_book. 
cur.execute("""CREATE TABLE rates_book
                (
                    id integer,
                    isbn varchar(13),
                    rating integer
                ) 
                 """)
 
# Create table reviews_list. 
cur.execute("""CREATE TABLE reviews_list 
                (
                    id integer,
                    name_list varchar(75),
                    date varchar(25),
                    text varchar(1000)
                ) 
                 """)

# Create table reviews_book. 
cur.execute("""CREATE TABLE reviews_book 
                (
                    id integer,
                    isbn varchar(13),
                    text varchar(1000)
                ) 
                 """)


# Commit changes and close the connection.
try:
    conn.commit()
except:
    conn.rollback()
    print('Could not commit changes... Rolling back and exiting...')
    exit(1)
finally:
    conn.close()


