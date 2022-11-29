import logging
import matplotlib.pyplot as plt

from db_operations import DbOperations # Database controller

log = logging.getLogger(__name__)

class PlotOperations:

    def __init__(self):
        self.plt = plt

    def basic_boxplot(self, year1:int, year2:int):
        sample_date = db.fetch_all_year((year1, year2))
        #min_temp = db.fetch_data("min_temp >= ? AND sample_date <= ?", (year1, year2))
        #max_temp = db.fetch_data("max_temp >= ? AND sample_date <= ?", (year1, year2))
        #avg_temp = db.fetch_data("avg_temp >= ? AND sample_date <= ?", (year1, year2))

        self.plt.title("Weather.gc.ca basic boxplot")
        self.plt.xlabel("Date")
        self.plt.yticks(range(0, 100, 1))

        self.plt.plot(sample_date, 0, '-.', label='Raw')
        #self.plt.plot(sample_date, min_temp, '-.', label='Raw')
        #self.plt.plot(sample_date, max_temp, '-.', label='Raw')
        #self.plt.plot(sample_date, avg_temp, '-.', label='Raw')

    def boxplot(self, data:dict):
        self.plt.legend()
        self.plt.show()
