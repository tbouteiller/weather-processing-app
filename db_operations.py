'''This module represents the database and the corresponding operations.'''
import sqlite3
from datetime import datetime
import os
import logging
import html
import json

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
                log.info("Table created successfully.")
                self.connection.commit()

        except Exception as e:
            print("Table already exists.")
            log.warning("Table already exists.")

    def save_data(self, weather_data):
        '''Saves all data from the weather table and prints each row.'''
        try:
            if self.connection is not None:
                for k, v in weather_data.items():
                    min = float(v['Min'])
                    max = float(v['Max'])
                    avg = float(v['Mean'])

                    query = '''insert into weather (html.escape(sample_date),
                    html.escape(location), html.escape(min_temp),
                    html.escape(max_temp), html.escape(avg_temp))
                    values ("' + k + '",' + f'"Winnipeg", {min}, {max}, {avg})'''

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
                    delete from sqlite_sequence where name = 'weather';
                """)
                self.connection.commit()
                print("Data has been purged successfully.")
                log.warning("Data has been purged successfully.")

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

    def fetch_all_year(self, year1, year2):
        '''
        Fetches all data rows in the weather dictionary in the
        date range provided.
        '''
        try:
            if self.connection is not None:
                rows = self.connection.cursor().execute("select * from weather").fetchall()
                for row in rows:
                    print(row)
                    log.info(row)
        except Exception as e:
            print("Error:", e)
            log.error("Error:", e)
