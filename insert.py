#!/usr/bin/env python

from goodreads import client
from sys import exit
import psycopg2
import random

# Did not want to import string.
lowercase = 'abcdefghijklmnopqrstuvwxyz'
numbers = '0123456789'

# Categories - Random samples to pick from.
categ = ['Drama', 'Sci-fi', 'Crime', 'Bio', 'Science', 'Adventure', 'Satire', 'Health', 'Guide', 'Childrens', 'Romance', 'Poetry', 'Travel']

NUM_BOOKS = 10 
OFFSET = 121

def load_book(title, isbn, year, pages, counter):
    '''
        Load a specific book into DB.

    '''
    cur.execute("""INSERT INTO books (title, isbn, year, pages) VALUES (
            %s,
            %s,
            %s,
            %s
            )
            """, (title, isbn, year, pages))
    print 'Loaded book No. {0}'.format(counter + 1)

def load_author(author):
    '''
        Load a specific author into DB

    '''
    cur.execute("""INSERT INTO authors (name, origin, born) VALUES (
            %s,
            %s,
            %s
            ) 
            """, (author.name, author.hometown, author.born_at))
            
# Rating extraction function from goodreads API into the DB      
def load_book_rating(book):
	'''
		Load the rating of the registered books int DB
	'''
	cur.execute("""INSERT INTO rates_book(isbn,rating) VALUES (
				%s,
				%s
				)
				""" , (book.isbn,book.average_rating)
				)

# Functions to create random passwords and emails for users.
def get_password():
    # Returns a random password 10 - 18 characters long.
    letters = ''.join(random.sample(lowercase, random.randint(8,14)))
    nums = ''.join(random.sample(numbers,random.randint(2,4)))
    return letters + nums

def get_email():
    # Returns a random email.
    letters = ''.join(random.sample(lowercase, random.randint(8,14)))
    nums = ''.join(random.sample(numbers,random.randint(2,4)))
    return letters + nums + '@mail.com'
    

# User registering function into the DB
def load_users(user):
	'''
		Load users into the user array of the DB
	'''
	cur.execute(""" INSERT INTO users (kind, username, password, email) VALUES (
				%s,
				%s,
                %s,
                %s
				)
				""" , ("registered user",user.user_name,get_password(), get_email())
				)

# Function to initiate table categories.
def load_categories(categ):
    """
        Load all categories present in 'categ' list.

    """
    for category in categ:
        cur.execute("""INSERT INTO categories VALUES (
                    %s,
                    %s
                    )  
                """, (category, random.randint(0,100000)))

# Function to fill table belongs_to.
def load_belongs_to(isbn, categ):
    '''
        Assign each book with isbn to a random category.

    '''
    cur.execute(""" INSERT INTO belongs_to (isbn, kind) VALUES (
                    %s,
                    %s
                    )
                """, (isbn, random.choice(categ))) 

				
# Connect to the database.
try:
    # Change 'xbaremenos' to your specific username and database name.
    conn = psycopg2.connect("dbname = 'xbaremenos' user = 'xbaremenos'")
except:
    print('Could not connect to DB... exiting...')
    exit(1)


# Try to connect to GoodReads DB through their API
try:
    gc = client.GoodreadsClient('eNOeZpRWitrj0rqo8B9Zg', 'EWTD4TLkL7VNnHjDsdh13JFvk7xkcT6P6CWFg6EJhc')
except:
    print 'Could not connect to goodReads API!'
    print 'exiting ./insert'
    exit(1)


# Create a cursor.
cur = conn.cursor()

# Create categories.
load_categories(categ)

loaded_books = 0
counter = 0
# Create some entries to books.
while loaded_books < NUM_BOOKS: 
    print 'Into book No. {0}'.format(counter + 1)
    
    try:
        book = gc.book((counter + 1) * OFFSET)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        # An error occured, move on to the next book.
        counter += 1
        continue

    title = book.title
    isbn = book.isbn
    year = book.publication_date[2]
    pages = book.num_pages
    
    if year != None:
        year = int(year)
    if pages != None:
        pages = int(pages)
    
    # Try to load book into DB. If title is too long, just ignore the book
    # and move on to the next one. 
    if len(title) > 100:
        counter += 1
        continue
    
    load_book(title, isbn, year, pages, counter)
    load_book_rating(book)
    loaded_books += 1
    counter += 1

    # Insert into belongs_to.
    load_belongs_to(isbn, categ)

    # Load associated author.
    try:
        author = gc.find_author(book.authors[0])
    except:
        print 'Could not associate an author with this book, moving on'
        continue
    
    load_author(author)
        

print 'Tried to load {0} books'.format(counter)
print 'Added a total of {0} books.'.format(loaded_books)


# Insert 4 admin users (ourselves)
cur.execute("""INSERT INTO users (kind, username, password, email) VALUES 
            (
                'admin',
                'xbaremenos',
                'l337H@ck4R!!1!',
                'charkops@auth.gr'
            )
        """)

cur.execute("""INSERT INTO users (kind, username, password, email) VALUES 
            (
                'admin',
                'maylo',
                'YoUCaNtF1nDTh1S',
                'antonodn@ece.auth.gr'
            )
        """)


cur.execute("""INSERT INTO users (kind, username, password, email) VALUES 
            (
                'admin',
                'Z4R0',
                'Th1S1SR4GuL@R',
                'ialevras@ece.auth.gr'
            )
        """)


cur.execute("""INSERT INTO users (kind, username, password, email) VALUES 
            (
                'admin',
                'No0Ne!1',
                'S3cR37P@ssw0RD',
                'dimivars@ece.auth.gr'
            )
        """)

# insert 6 registered users into the DB
NUM_USERS = 6
counter = 0
loaded_users = 0

while loaded_users < NUM_USERS :
    print 'Into users No. %s' % (counter + 1)
	
    try:
	    user = gc.user((counter + 1))
    except KeyboardInterrupt:
	    raise KeyboardInterrupt
    except:
        counter += 1
        continue
		
    if not user.user_name:
        print 'EMPTY NAME !'
        counter += 1
        continue

    print 'Trying to load user No. %s' %(counter + 1)
    load_users(user)
 
	
    loaded_users += 1
    # increment the counter value
    counter += 1
    
print 'Total users loaded = %s' % loaded_users

# Commit changes and close connection, exit programm.
try:
    conn.commit()
except:
    conn.rollback()
    print('Could not commint changes... rolling back...')
    exit(1)
finally:
    conn.close()




