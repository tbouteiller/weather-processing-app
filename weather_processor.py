"""
Class that contains UI code for weather-processing-app
Created by: David & Tanner
"""
import logging
import os
from appdirs import *

from scrape_weather import WeatherScraper
from db_operations import DbOperations
from plot_operations import PlotOperations


class WeatherProcessor():
    """
    A class to control all UI elements.
    """
    def __init__(self):
        self.w = WeatherScraper()
        self.db = DbOperations()
        self.pt = PlotOperations()

        self.appname = "weather-processing-app"
        self.appauthor = "weather-processing-app"


    def logging_init(self):
        """
        Sets up the logging for the rest of the program, setting log files
        to end up in either
        """
        try:
            if os.name == "posix":
                logging.basicConfig(format="%(levelname)s %(asctime)s: %(message)s",
                                    datefmt="(%a)%d/%m/%Y %H:%M:%S",
                                    filename=f"{unix_log_dir}/info.log",
                                    level=logging.INFO)

            else:
                logging.basicConfig(format="%(levelname)s %(asctime)s: %(message)s",
                                    datefmt="(%a)%d/%m/%Y %H:%M:%S",
                                    filename="info.log",
                                    level=logging.INFO)
        except Exception as e:
            print("Error creating log file: ", e)

    def db_init(self):
        """
        Initializes the DB.
        """
        self.db.initalize_db()

    def ui_init(self):
        """
        Holds the main terminal UI loop.
        """
        print("Welcome to the weather-processing-app \o.o/")
        user_input = ""

        while user_input != "0":
            print("""
                Options:
                S = Scrape and download all weather data
                P = Purge all weather data

                B = Show a boxplot between a number of years
                L = Show a lineplot for a specific month/year

                0 = Exit the program
                """)
            user_input = input("Please select an option (S,P,B,L,0): ")

            if user_input == "S".upper():
                self.w.scrape()
                self.db.save_data(self.w.weather)
            elif user_input == "P".upper():
                self.db.purge_data()
            elif user_input == "B".upper():
                year2 = input("\nPlease enter the start year:")
                year1 = input("\nPlease enter the end year:")
                self.pt.basic_boxplot(self.db, year1, year2)
            elif user_input == "L".upper():
                year = input("\nPlease enter the year:")
                month = input("\nPlease enter the month:")
                self.pt.lineplot(self.db, year, month)

if __name__ == "__main__":
    weather = WeatherProcessor()

    weather.logging_init()
    weather.db_init()
    weather.ui_init()
