import psycopg2

# Simple script used to drop the projects database

conn = psycopg2.connect(
	database="postgres", user='postgres', password='admin', host='127.0.0.1', port='5432'
)

conn.autocommit = True

cursor = conn.cursor()

# Drop the database
dropDatabase = '''DROP DATABASE trafficmanagement;'''

cursor.execute(dropDatabase)

conn.commit()
conn.close()
