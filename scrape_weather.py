'''This module will scrape the weather data from the GC climate weather website.'''
from bs4 import BeautifulSoup
from datetime import date
import requests

class WeatherScraper:
    '''A class which scrapes weather data using Beautiful Soup and stores data within a weather dictionary.'''
    def __init__(self) -> None:
        self.weather = {}
        self.month = date.today().month
        self.year =  date.today().year
        self.url = f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year={self.year}&Month={self.month}#"
        self.soup = self.start_soup()
        self.prevous_month = True

    def start_soup(self):
        '''Peforms get request and initalizes the BeautifulSoup parser. Automatically runs once when the WeatherScraper class is initalized.'''
        return BeautifulSoup(requests.get(self.url).content, 'html.parser')

    def scrape(self): 
        '''Scrapes the weather data by targeting the daily Max, Min, and Mean temperatures for each month.'''
        while self.prevous_month is True:    
            print(f"Scraping weather data for: {self.year}-{self.month}")
            
            for row in self.soup.find('table').find_all("tr")[1:-4]:
                index = 0
                key = ""
                daily_temp = {}

                for item in row.find_all("th"):
                    if item.text.strip() and item.name == "th":
                        key = f"{self.year}-{self.month}-{item.text.strip()}"  
                    
                for item in row.find_all("td")[0:3]:
                    conditions = ["Max", "Min", "Mean"]

                    if item.text.strip() and item.name == "td":
                        daily_temp[conditions[index]] = item.text.strip()
                        self.weather[key] = daily_temp
                        index = index + 1

            self.check_for_previous_month()
        
    def check_for_previous_month(self):
        '''Checks if data for previous month is available. Will update the url and rerun the soup if true.'''
        address = self.soup.find(rel="prev", href=True) 
     
        if address and not self.soup.find("li", {"class": "previous disabled"}):
            self.url = f'https://climate.weather.gc.ca{address.get("href")}'
            self.year =  self.url[self.url.index("&Year=") + 6: self.url.index("&M")]
            self.month = self.url[self.url.index("Month=") + 6:]
            self.soup = self.start_soup()
            self.prevous_month = True
        else:
            self.prevous_month = False
            
    def print_weather_data(self):
        '''Returns a string representation of the weather dictionary.'''
        return print(self.weather)

# Testing things
test = WeatherScraper()
test.scrape()
test.print_weather_data()