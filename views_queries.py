import psycopg2
from sys import exit

# Connect to the database.

try:
    conn = psycopg2.connect("dbname = 'mydb' user = 'm4yl0'")
except:
    print('Could not connect to DB... exiting...')
    exit(1)
    
# create cursor 

cur = conn.cursor()

# TOP SUGGESTIONS VIEW that prints the three latest suggestions depending on the date

cur.execute("""CREATE VIEW Top_suggestions AS
					SELECT title
					FROM suggestions
					ORDER BY suggestions.date DESC
					LIMIT 3
										  """)
					  
# fetched all the view table

cur.execute("""SELECT * FROM Top_suggestions""")
top_suggestions= cur.fetchall()
print 'The three latest book suggestion based on the date are : '
for i in range(0,len(top_suggestions)):
	print '\n %s' %top_suggestions[i]
# Average rating

cur.execute("""CREATE VIEW Average_score AS
							SELECT books.title,books.isbn,AVG(rates_book.rating)
							FROM books,rates_book
							WHERE books.isbn = rates_book.isbn
							GROUP BY books.isbn
			""")
			
cur.execute("""SELECT * FROM Average_score""")
score = cur.fetchall()

print 'The average score of each book is : '

for i in range(0,len(score)):
	print score[i]
	print '\n'
