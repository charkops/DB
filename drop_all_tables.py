#!/usr/bin/env python

"""
    Quick way to drop all tables
    and create the Schema from start.

"""

import psycopg2
import sys

# Connect to DB.
try:
    conn = psycopg2.connect("dbname = 'xbaremenos' user = 'xbaremenos'")
except:
    print('Could not connect to DB, exiting...')

cur = conn.cursor()

cur.execute('DROP SCHEMA public CASCADE')
cur.execute('CREATE SCHEMA public')
cur.execute('GRANT ALL ON SCHEMA public TO postgres')
cur.execute('GRANT ALL ON SCHEMA public TO public')


# Clone connection.
conn.commit()
conn.close()
