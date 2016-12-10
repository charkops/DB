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
                    isbn varchar(15),
                    year integer,
                    pages integer
                ) 
                """) 

# Create table authors.
cur.execute("""CREATE TABLE authors
                (
                    id serial,
                    name varchar(50),
                    origin varchar(50),
                    born varchar(20)
                ) 
                 """)

# Create table users.
cur.execute("""CREATE TABLE users
                (
                    id serial,
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
                    date varchar(25)
                ) 
                 """)

# Create table publishers.
cur.execute("""CREATE TABLE publishers 
                (
                    name varchar(75),
                    location varchar(50),
                    established varchar(25)
                ) 
                 """)

# Create table suggestions.
cur.execute("""CREATE TABLE suggestions 
                (
                    title varchar(75),
                    date varchar(25)
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


