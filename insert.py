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

# Publishers names.
pub_names = ['OMG books. Inc.','LOL books. Inc.', 'KEK books. Inc.', 'JK books. Inc.']

# Lists names.
lists_names = ['My top 10 favourite Sci-fi books', 'Poems from the Spanish Civil War', '21 adventure books you should read before you die']

# Suggestions dates.
sug_dates = ['10-2-2016', '10-2-1994', '11-6-2005', '11-6-2001']

# Dictionary for keeping track of lists name-date connection.
lists_dict = {'My top 10 favourite Sci-fi books' : '2012-02-06', 'Poems from the Spanish Civil War' : '2013-11-21', '21 adventure books you should read before you die' : '2011-10-11'}

# Temp books isbn.
books_isbn = []

# Random list names

NUM_USERS = 6
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
		Load the rating of the registered books into DB
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
					
# Function to fill table writes.
def load_writes(isbn, author_id):
    '''
        Assign each book with isbn to an author_id.

    '''
    cur.execute(""" INSERT INTO writes (isbn, author_id) VALUES (
                    %s,
                    %s
                    )
                """, (isbn, author_id)) 			

# Function to fill table suggestions.
def load_suggestions():
    """
        Load 4 hardcoded suggestions. Not much time left :)

    """
    cur.execute("""INSERT INTO suggestions (title, date) VALUES (
                    'Top 10 books to stay fit.',
                    '10-2-2016'
                )""" )

    cur.execute("""INSERT INTO suggestions (title, date) VALUES (
                    'Keeping up with the New generation',
                    '10-2-1994'
                )""" )

    cur.execute("""INSERT INTO suggestions (title, date) VALUES (
                    'Introduction to Pen Testing',
                    '11-6-2005'
                )""" )
    
    cur.execute("""INSERT INTO suggestions (title, date) VALUES (
                    'Is cyberpunk the new meta?',
                    '11-6-2001'
                )""" )

# Function to fill table publishers.
def load_publishers():
    """
        Load 4 hardcoded publishers. Still no time :)
        
    """
    cur.execute("""INSERT INTO publishers (name, location, established) VALUES(
                    'OMG books. Inc.',
                    'NYC, New York',
                    '4/2/1941'
                )        
                """)

    cur.execute("""INSERT INTO publishers (name, location, established) VALUES(
                    'LOL books. Inc.',
                    'Portland, New Mexico',
                    '13/5/1914'
                )        
                """)

    cur.execute("""INSERT INTO publishers (name, location, established) VALUES(
                    'KEK books. Inc.',
                    'Thessaloniki, Greece',
                    '12/5/1968'
                )        
                """)

    cur.execute("""INSERT INTO publishers (name, location, established) VALUES(
                    'JK books. Inc.',
                    'Athens, Greece',
                    '21/7/1984'
                )        
                """)

# Funtion to fill table published.
def load_published(isbn):
    """
        Assign each book (through their isbn) a publisher and a published_id

    """
    cur.execute("""INSERT INTO published (isbn, publisher_name, published_id) VALUES (
                    %s,
                    %s,
                    %s
                    )
                """, (isbn, random.choice(pub_names), random.randint(1,10)))


# Function to fill table rates_list.
def load_rates_list(user_id):
    """
        Assign a rating to some list given a user_id.

    """
    random_name = random.choice(lists_names)
    cur.execute("""INSERT INTO rates_list (id, name_list, date, rating) VALUES(
                    %s,
                    %s,
                    %s,
                    %s
                    )
                """, (user_id, random_name, lists_dict[random_name], random.randint(1,10) ))


# Function to fill table in_suggestions.
def load_in_suggestion(isbn, loaded_books):
    """
        Given the isbn of a book. Insert values to table in_suggestion.

    """
    cur.execute("""INSERT INTO in_suggestion (date, isbn, num_items) VALUES (
                    %s,
                    %s,
                    %s
                )
                """, (random.choice(sug_dates), isbn, random.randint(1,loaded_books)))

# Random string generator 1 - 1000 characters.
def random_text(length):
    string = ''
    for i in range(1,random.randint(1,length)):
        string += random.choice(lowercase)

    return string


# Function to fill table reviews_book.
def load_reviews_book(user_id):
    """
        Choose a book to review, given a user_id. Generate random text as review.
        
    """
    cur.execute("""INSERT INTO reviews_book (id, isbn, text) VALUES (
                    %s,
                    %s,
                    %s
                )
                """, (user_id, random.choice(books_isbn), random_text(1000)))



# Function to fill table reviews_list.
def load_reviews_list(user_id):
    """
        Give a random review in a random list, given a user_id.
    
    """
    random_name = random.choice(lists_names)
    cur.execute("""INSERT INTO reviews_list (id, name_list, date, text) VALUES (
                    %s,
                    %s,
                    %s,
                    %s
                )
                """, (user_id, random_name, lists_dict[random_name], random_text(1000)))


# Function to fill table suggest.
def load_suggest(user_id):
    """
        Takes user_id as argument and fills the table with a random date.
    
    """
    cur.execute("""INSERT INTO suggest (user_id, date) VALUES (
                %s,
                %s
                )
                """, (user_id, random.choice(sug_dates))) 




    ########################
    #### ---- MAIN ---- ####
    ########################
   

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

# Load publishers.
load_publishers()

# Load suggestions.
load_suggestions()


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
    books_isbn.append(isbn)

    # Insert into belongs_to.
    load_belongs_to(isbn, categ)
    # Insert into published. 
    load_published(isbn)

    # Load associated author.
    try:
        author = gc.find_author(book.authors[0])
    except:
        print 'Could not associate an author with this book, moving on'
        continue
    
    load_author(author)
    load_writes(isbn, loaded_books) 
    load_in_suggestion(isbn, loaded_books)

print 'Tried to load {0} books'.format(counter)
print 'Added a total of {0} books.'.format(loaded_books)


# Insert 4 admin users (ourselves)
# This could be wrapped up in a function. Will do if i find time.
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

# insert registered users into the DB
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

    load_reviews_book(loaded_users)
    
print 'Total users loaded = %s' % loaded_users


# FILL THE LISTS TABLE IN OUR DATABASE
	
cur.execute("""INSERT INTO lists (user_id,name,date,kind) VALUES 
            (
                6,
                'My top 10 favourite Sci-fi books',
                '2012-02-06',
                'Sci-fi'
            );
        """)


cur.execute("""INSERT INTO lists (user_id,name,date,kind) VALUES 
            (
                4,
                'My top 10 favourite Sci-fi books',
                '2013-02-06',
                'Sci-fi'
            );
        """)
cur.execute("""INSERT INTO lists (user_id,name,date,kind) VALUES 
            (
                '5',
                'Poems from the Spanish Civil War',
                '2013-11-21',
                'Poetry'
            );
        """)
cur.execute("""INSERT INTO lists (user_id,name,date,kind) VALUES 
            (
                '8',
                '21 adventure books you should read before you die',
                '2011-10-11',
                'Adventure'
            );
        """)
        
print('Loaded lists')

for i in range(loaded_users):
    load_rates_list(i + 1)
    load_reviews_list(i + 1)
    load_suggest(i + 1)

print('Loaded rates_list')


# ROLES PART OF OUR DATABASE


# Simple example for "any" registered user role 
cur.execute(""" CREATE ROLE registered_user WITH PASSWORD 'abcdpassruser123'""")
cur.execute("""ALTER ROLE registered_user WITH LOGIN""")

cur.execute("""GRANT SELECT ON books,authors,lists,publishers,reviews_book,reviews_list TO registered_user""")
cur.execute("""GRANT INSERT ON lists TO registered_user""")

# Simple example for "each" of the admins set in the database role
cur.execute(""" CREATE ROLE administrator WITH PASSWORD 'admin123password'""")
cur.execute("""ALTER ROLE administrator WITH LOGIN""")

cur.execute("""GRANT SELECT , INSERT , UPDATE ,DELETE ON books,authors,users,lists,publishers,suggestions,writes,categories,
								published,in_suggestion,reviews_book,reviews_list,rates_book,rates_list,suggest,
								writes TO administrator""")




# Commit changes and close connection, exit programm.
try:
    conn.commit()
except:
    conn.rollback()
    print('Could not commint changes... rolling back...')
    exit(1)
finally:
    conn.close()




