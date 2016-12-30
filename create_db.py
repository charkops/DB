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

# Create table lists.
cur.execute("""CREATE TABLE lists 
                (
                    user_id integer REFERENCES users (id),
                    name varchar(75),
                    date varchar(25),
                    kind varchar(25),
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

# Create table writes.
cur.execute("""CREATE TABLE writes 
                (
                    isbn varchar(13) REFERENCES books (isbn),
                    author_id integer REFERENCES authors (id)
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
                    isbn varchar(13) REFERENCES books (isbn),
                    publisher_name varchar(75) NOT NULL REFERENCES publishers (name),
                    published_id integer,
                    CHECK (publisher_name != ''),
                    CHECK (published_id > 0)
                ) 
                 """)


# Create function getTotalRegBooks().
cur.execute("""CREATE FUNCTION getTotalRegBooks() RETURNS bigint AS $$
                    SELECT COUNT(*) FROM books;
                    $$ LANGUAGE SQL;
                """)

# Create table in_suggestion.
cur.execute("""CREATE TABLE in_suggestion
                (
                    date varchar(25) REFERENCES suggestions (date),
                    isbn varchar(13) REFERENCES books (isbn),
                    num_items integer,
                    CHECK (num_items >= 0 AND (num_items <= getTotalRegBooks()))
                ) 
                 """)

# Create table rates_book. 
cur.execute("""CREATE TABLE rates_book
                (
                    id integer REFERENCES users(id),
                    isbn varchar(13) REFERENCES books(isbn),
                    rating numeric,
                    CHECK (rating >= 0 AND rating <= 10)
                ) 
                 """)
 
# Create table rates_list. 
cur.execute("""CREATE TABLE rates_list 
                (
                    id integer REFERENCES users(id),
                    name_list varchar(75),
                    date varchar(25),
                    rating numeric,
                    FOREIGN KEY (name_list, date) REFERENCES lists (name, date)
                ) 
                 """)

# Create table reviews_list. 
cur.execute("""CREATE TABLE reviews_list 
                (
                    id integer REFERENCES users (id),
                    name_list varchar(75),
                    date varchar(25),
                    text varchar(1000),
                    FOREIGN KEY (name_list, date) REFERENCES lists (name, date)
                ) 
                 """)

# Create table reviews_book. 
cur.execute("""CREATE TABLE reviews_book 
                (
                    id integer REFERENCES users (id),
                    isbn varchar(13) REFERENCES books (isbn),
                    text varchar(1000)
                ) 
                 """)

# Create function getTotalUsersNum().
cur.execute("""CREATE FUNCTION getTotalUsersNum() RETURNS bigint AS $$
                    SELECT COUNT(*) FROM users;
                    $$ LANGUAGE SQL;
                """)

# Create table suggest. 
cur.execute("""CREATE TABLE suggest 
                (
                    user_id integer REFERENCES users (id),
                    date varchar(25) REFERENCES suggestions (date),
                    CHECK (user_id > 0 AND (user_id <= getTotalUsersNum()))
                ) 
                 """)

# Create table belongs_to. 
cur.execute("""CREATE TABLE belongs_to 
                (
                    isbn varchar(13) REFERENCES books (isbn),
                    kind varchar(25) REFERENCES categories (category)
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


