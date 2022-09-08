import psycopg2
from django.core.management import call_command
from django.core.management.base import BaseCommand

# Command script used to create the project Database, make migrations, migrate and load the users present in users.json

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        #self.createDB()
        call_command("makemigrations")
        call_command("migrate")
        call_command("loaddata", "users.json")

    # def createDB(self):
    #     conn = psycopg2.connect(
    #         database="postgis", user='postgis', password='postgis', host='db', port='5432'
    #     )
    #
    #     conn.autocommit = True
    #
    #     # Creating a cursor object using the cursor() method
    #     cursor = conn.cursor()
    #
    #     # Preparing query to create a database
    #     createDatabase = '''CREATE DATABASE trafficmanagement;'''
    #
    #     cursor.execute(createDatabase)
    #
    #     conn.commit()
    #     conn.close()
