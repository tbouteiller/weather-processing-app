'''This module represents the database and the corresponding operations.'''
import sqlite3
from datetime import datetime
import os
import logging

log = logging.getLogger(__name__)

class DbOperations:
    '''This class represents the weather sqlite database and contains various methods that run queries.'''

    def __init__(self):
        '''Class constructor which trys to establish a connection when initalzied.'''
        self.connection = None
        self.initalize_db()

        if self.connection is None:
            try:
                self.connection = sqlite3.connect('weather.sqlite')
                print("Connection successful.")
                log.info("Connection successful.")
            except Exception as e:
                print("Error connecting to database: ", e)
                log.error("Error connecting to database: ", e)

    def __del__(self):
        '''Destructor used to dispose of connection.'''
        self.connection.cursor()
        self.connection.close()

    def initalize_db(self):
        '''Initalizes the database with the default table if there is a connection open.'''

        try:
            if self.connection is not None:
                self.connection.cursor()
                self.connection.execute("""create table weather
                                            (id integer primary key autoincrement not null,
                                            sample_date text not null unique,
                                            location text not null,
                                            min_temp real not null,
                                            max_temp real not null,
                                            avg_temp real not null);""")
                log.warning("Table created successfully.")
                self.connection.commit()

        except Exception as e:
            print("Table already exists.")
            log.info("Table already exists.")

    def save_data(self, weather_data:dict):
        '''Saves all data from the weather table and prints each row.'''

        try:
            if self.connection is not None:
                for k, v in weather_data.items():

                    min = float(v['Min'])
                    max = float(v['Max'])
                    avg = float(v['Mean'])
                    query = 'insert into weather (sample_date, location, min_temp, max_temp, avg_temp) values ("' + k + '",' + f'"Winnipeg", {min}, {max}, {avg})'

                    self.connection.execute(query)
                    self.connection.commit()
                print("Added data successfully.")
                log.info("Added data successfully.")

        except Exception as e:
            print("Error:",e)
            log.error("Error:",e)

    def purge_data(self):
        '''Deletes all records from the weather table.'''
        try:
            if self.connection is not None:
                self.connection.executescript("""
                    delete from weather;
                    delete from sqlite_sequence where name='weather;'
                """)
                self.connection.commit()
                print("Data has been purged successfully.")
                log.info("Data has been purged successfully.")

        except Exception as e:
            print("Error", e)
            log.error("Error", e)

    def fetch_data(self):
        '''Fetches all data rows from the weather dictionary.'''
        try:
            if self.connection is not None:
                rows = self.connection.cursor().execute("select * from weather").fetchall()
                for row in rows:
                    print(row)
                    log.info(row)
        except Exception as e:
            print("Error:", e)
            log.error("Error:", e)

#db = DbOperations()
#db.initalize_db()

#dummy data for testing
#data = {"2023-01-01": {'Max': '3.5', 'Min': '12.8', 'Mean': '8.2'}, "2024-01-01": {'Max': '95', 'Min': '28', 'Mean': '6'}}
#db.save_data(data)
#db.fetch_data()
#db.purge_data()
#db.fetch_data()
