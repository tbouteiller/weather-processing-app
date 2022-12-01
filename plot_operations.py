import logging
import matplotlib.pyplot as plt

from db_operations import DbOperations

log = logging.getLogger(__name__)

class PlotOperations:

    def __init__(self):
        self.plt = plt

        self.min_temp = []
        self.max_temp = []
        self.avg_temp = []
        self.date = []

    def basic_boxplot(self, db, year1:int, year2:int):
        #self.plt.boxplot(self.date, [self.min_temp, self.max_temp, self.avg_temp])
        #self.plt.yticks(range(0, 100, 1))
        #self.plt.tight_layout()
        #self.plt.tick_params(axis='x', which='major', labelsize=5)
        return "Not implemented yet"

    def lineplot(self, db, year:int, month:int):
        data = []
        date = f"{year}-{month}-01"

        if(month == "01"):
            date_range = f"{year}-{month}-31"
        elif(month == "02"):
            date_range = f"{year}-{month}-28"
        elif(month == "03"):
            date_range = f"{year}-{month}-31"
        elif(month == "04"):
            date_range = f"{year}-{month}-30"
        elif(month == "05"):
            date_range = f"{year}-{month}-31"
        elif(month == "06"):
            date_range = f"{year}-{month}-30"
        elif(month == "07"):
            date_range = f"{year}-{month}-31"
        elif(month == "08"):
            date_range = f"{year}-{month}-31"
        elif(month == "09"):
            date_range = f"{year}-{month}-30"
        elif(month == "10"):
            date_range = f"{year}-{month}-31"
        elif(month == "11"):
            date_range = f"{year}-{month}-30"
        elif(month == "12"):
            date_range = f"{year}-{month}-31"

        data = db.fetch_all_months(date, date_range)

        self.plt.title("Weather.gc.ca basic boxplot")
        self.plt.xlabel("Date")
        self.plt.xticks(rotation=45, ha='right', fontsize = 12)

        for i in data:
            self.date.append(i[1])
            self.avg_temp.append(i[5])

        self.plt.plot(self.date, self.avg_temp,'-.', label='Average Temp')

        self.plt.legend()
        self.plt.show()
