#!/usr/bin/env python

import psycopg2
from sys import exit, stdout

# Connect to the database.
try:
    # Change 'xbaremenos' to your specific username and database name.
    conn = psycopg2.connect("dbname = 'xbaremenos' user = 'xbaremenos'")
except:
    print('Could not connect to DB... exiting...')
    exit(1)


# Create a cursor.
cur = conn.cursor()

# Helper print function.
def printResults():
    try:
        rows = cur.fetchall()
    except psycopg2.ProgrammingError:
        print('Nothing to return')
        return

    for row in rows:
        for columns in row:
            stdout.write(str(columns))
            stdout.write(' ' * 4)
        print('')
    print('')

# Create queries.

# 1.) Select the isbn of the books writen by author with id = 7; (7 is random, could be anything)
cur.execute("""SELECT isbn FROM writes 
                WHERE author_id = 7
            """)
print('Que No. 1\n')
printResults()

# 2.) Select the title of the book given its isbn.
cur.execute("""SELECT title FROM books 
                WHERE isbn = '0307277674'
            """)            
                
print('Que No. 2\n')
printResults()

# 3.) Select the isbn of books published by puslisher 'OMG books.' OR 'KEK books.'
cur.execute("""SELECT isbn FROM published 
                WHERE publisher_name = 'OMG books. Inc.'
                UNION
                SELECT isbn FROM published
                WHERE publisher_name = 'KEK books. Inc.'
            """)
print('Que No. 3\n')
printResults()

# 4.) Select id, name from authors, the isbn and title of the books that he/she has writen.
cur.execute("""SELECT authors.id, authors.name, writes.isbn, books.title FROM authors, writes, books
                WHERE authors.id = writes.author_id AND books.isbn = writes.isbn
            """)
print('Que No. 4\n')
printResults()

# 5.) Update a row in table rates_book. Change the rating made by a specific user.
cur.execute("""UPDATE rates_book SET rating = 7 WHERE isbn = '1597770086'
            """)
print ('Que No. 5\n')
printResults()

# 6.) Select num_items from table in_suggestion that belong to a suggestion made at a specific date.
cur.execute("""SELECT SUM(num_items) FROM in_suggestion WHERE date = '11-6-2005'""")
print('Que No. 6\n')
printResults()

# 7.) Select text review of book with isbn = ..., made by user with name = ...
cur.execute("""SELECT text FROM reviews_book WHERE id = 5 AND isbn = '0307277674'""")
print('Que No. 7\n')
printResults()


# Commit changes and close the connection.
try:
    conn.commit()
except:
    conn.rollback()
    print('Could not commit changes... Rolling back and exiting...')
    exit(1)
finally:
    conn.close()
