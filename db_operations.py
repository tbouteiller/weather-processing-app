'''This module represents the database and the corresponding operations.'''
import sqlite3
import datetime
import logging
import calendar

log = logging.getLogger(__name__)

class DbOperations:
    '''
    This class represents the weather sqlite database
    and contains various methods that run queries.
    '''

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
                                            sample_date date not null unique,
                                            location text not null,
                                            min_temp real not null,
                                            max_temp real not null,
                                            avg_temp real not null);""")
                log.info("Table created successfully.")
                self.connection.commit()

        except Exception as e:
            print("Table already exists.")
            log.warning("Table already exists.", e)

    def save_data(self, weather_data: dict):
        '''Saves all data from the weather table and prints each row.'''
        try:
            if self.connection is not None:
                for k,value in weather_data.items():

                    try:
                        minimum = float(value['Min'])
                        maximum = float(value['Max'])
                        average = float(value['Mean'])
                    except KeyError:
                        minimum = 0.0
                        maximum = 0.0
                        average = 0.0

                    query = """insert into weather (sample_date, location, min_temp, max_temp, avg_temp) values (?, ?, ?, ?, ?);"""
                    self.connection.execute(
                        query, (k, "Winnipeg", minimum, maximum, average))
                    self.connection.commit()

                print("Added data successfully.")
                log.info("Added data successfully.")

        except Exception as e:
            print("Error:", e)
            log.error("Error:", e)

    def purge_data(self):
        '''Deletes all records from the weather table.'''
        try:
            if self.connection is not None:
                self.connection.executescript(
                    """delete from weather;delete from sqlite_sequence where name = 'weather';""")
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

    def fetch_all_years(self, year1, year2):
        '''
        Fetches all data rows in the weather dictionary in the
        date range provided.
        '''
        try:
            if self.connection is not None:
                avg = {
                    "01": [],
                    "02": [],
                    "03": [],
                    "04": [],
                    "05": [],
                    "06": [],
                    "07": [],
                    "08": [],
                    "09": [],
                    "10": [],
                    "11": [],
                    "12": []}

                if year2 == datetime.date.today().year:
                    month = datetime.date.today().month
                else:
                    month = 12

                year2 = f"{year2}-{str(month)}-{calendar.monthrange(int(year2), month)[1]}"
                year1 = f"{year1}-01-{calendar.monthrange(int(year1), 1)[1]}"
                rows = self.connection.cursor().execute(
                    "select * from weather WHERE sample_date <= ? AND sample_date >= ? ORDER BY id",
                    (year2, year1)).fetchall()

                for value in rows:
                    month = value[1].split("-")[1]
                    avg[month] += [value[5]]
                    log.info(rows)

                return avg

        except Exception as e:
            print("Error:", e)
            log.error("Error:", e)

    def fetch_all_months(self, date: str, date_range: str):
        '''
        Fetches all data rows in the weather dictionary in the
        date range provided.
        '''
        try:
            data = []
            if self.connection is not None:
                rows = self.connection.cursor().execute(
                    "select * from weather WHERE sample_date <= ? AND sample_date >= ? ORDER BY id",
                    (date_range, date)).fetchall()
                for value in rows:
                    data.append(value)
                    log.info(value)
                return data
        except Exception as e:
            print("Error:", e)
            log.error("Error:", e)
