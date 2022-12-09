import logging
import matplotlib.pyplot as plt
import calendar

log = logging.getLogger(__name__)


class PlotOperations:

    def __init__(self):
        self.plt = plt

        self.min_temp = []
        self.max_temp = []
        self.avg_temp = []
        self.date = []

    def basic_boxplot(self, db, year1: int, year2: int):
        '''
        Creates a boxplot of mean temperatures for all months
        between two specified years.
        '''
        box_data = db.fetch_all_years(year2, year1)
        labels, data = [*zip(*box_data.items())]

        plt.boxplot(data)
        plt.xticks(range(1, len(labels) + 1), labels)
        plt.show()

    def lineplot(self, db, year: str, month: str):
        data = []

        if '0' in month and "10" != month:
            new_month = str(month).replace("0", "")
        new_month = int(month)

        date = f"{year}-{month}-01"
        date_range = f"{year}-{month}-{calendar.monthrange(int(year), new_month)[1]}"

        data = db.fetch_all_months(date, date_range)

        self.plt.title("Weather.gc.ca basic boxplot")
        self.plt.xlabel("Date")
        self.plt.xticks(rotation=45, ha='right', fontsize=12)

        for i in data:
            self.date.append(i[1])
            self.avg_temp.append(i[5])

        self.plt.plot(self.date, self.avg_temp, '-.', label='Average Temp')

        self.plt.legend()
        self.plt.show()
