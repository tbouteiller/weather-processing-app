from scrape_weather import WeatherScraper
from db_operations import DbOperations
from plot_operations import PlotOperations

import logging
from appdirs import *
import os

appname = "weather-processing-app"
appauthor = "Tanner/David"

unix_log_dir = ""
windows_log_dir = ""
user_log = user_log_dir(appname, appauthor)

try:
    if os.name == "posix":
        if not os.path.exists(user_log):
            os.makedirs(user_log)
            logging.basicConfig(
                format="%(levelname)s %(asctime)s: %(message)s",
                datefmt="(%a)%d/%m/%Y %H:%M:%S",
                filename=f"{user_log}/info.log",
                level=logging.INFO)
        else:
            logging.basicConfig(
                format="%(levelname)s %(asctime)s: %(message)s",
                datefmt="(%a)%d/%m/%Y %H:%M:%S",
                filename=f"{user_log}/info.log",
                level=logging.INFO)

    else:
        if not os.path.exists(user_log):
            os.makedirs(user_log)
            logging.basicConfig(
                format="%(levelname)s %(asctime)s: %(message)s",
                datefmt="(%a)%d/%m/%Y %H:%M:%S",
                filename=f"{user_log}\\info.log",
                level=logging.INFO)
        else:
            logging.basicConfig(
                format="%(levelname)s %(asctime)s: %(message)s",
                datefmt="(%a)%d/%m/%Y %H:%M:%S",
                filename=f"{user_log}\\info.log",
                level=logging.INFO)

except Exception as e:
    print("Error creating log file: ", e)

# Test output
w = WeatherScraper()
db = DbOperations()
pt = PlotOperations()

w.scrape()
db.initalize_db()
db.purge_data()
db.save_data(w.weather)
# db.fetch_data()

pt.basic_boxplot(db, 2021, 2020)
pt.lineplot(db, "2021", "01")
