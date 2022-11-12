from scrape_weather import WeatherScraper
from db_operations import DbOperations
import logging
from appdirs import *
import os
import time
import getpass

appname = "weather-processing-app"
appauthor = "Tanner/David"

try:
    if os.name == "posix":
        if not os.path.exists(user_log_dir(appname, appauthor)):
            unix_log_dir = user_log_dir(appname, appauthor)
            os.makedirs(unix_log_dir)
            logging.basicConfig(format="%(levelname)s %(asctime)s: %(message)s",
                                datefmt="(%a)%d/%m/%Y %H:%M:%S",
                                filename=f"{unix_log_dir}/info.log",
                                level=logging.INFO)
        else:
            unix_log_dir = user_log_dir(appname, appauthor)
            logging.basicConfig(format="%(levelname)s %(asctime)s: %(message)s",
                                datefmt="(%a)%d/%m/%Y %H:%M:%S",
                                filename=f"{unix_log_dir}/info.log",
                                level=logging.INFO)

    else:
        if not os.path.exists(user_log_dir(appname, appauthor)):
            windows_log_dir = user_log_dir(appname, appauthor)
            os.makedirs(windows_log_dir)
            logging.basicConfig(format="%(levelname)s %(asctime)s: %(message)s",
                                datefmt="(%a)%d/%m/%Y %H:%M:%S",
                                filename=f"{windows_log_dir}\\info.log",
                                level=logging.INFO)
        else:
            windows_log_dir = user_log_dir(appname, appauthor)
            logging.basicConfig(format="%(levelname)s %(asctime)s: %(message)s",
                                datefmt="(%a)%d/%m/%Y %H:%M:%S",
                                filename=f"{windows_log_dir}\\info.log",
                                level=logging.INFO)
except Exception as e:
    print("Error creating log file: ", e)


test = WeatherScraper()
db = DbOperations()

test.scrape()
db.initalize_db()
db.fetch_data(test.weather)
