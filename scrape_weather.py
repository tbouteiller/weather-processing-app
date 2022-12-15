'''
This module will scrape the weather data
from the GC climate weather website.
Created by: David & Tanner
'''
from datetime import date
import logging
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

log = logging.getLogger(__name__)

class WeatherScraper:
    '''
    A class which scrapes weather data using Beautiful Soup
    and stores data within a weather dictionary.
    '''

    def __init__(self) -> None:

        self.weather = {}
        self.month = date.today().month
        self.year = date.today().year
        self.url = f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year={self.year}&Month={self.month}#"
        self.previous_month = True

    def scrape(self):
        '''
        Scrapes the weather data by targeting the daily Max, Min
        and Mean temperatures for each month.
        '''
        session = self.set_session()

        try:
            while self.previous_month is True:
                try:
                    soup = BeautifulSoup(session.get(self.url).content, 'html.parser')
                except Exception as e:
                    print('Error:', e)
                    log.error('Error:', e)
                    session.close()
                    return

                print(f"Scraping weather data for: {self.year}-{self.month}")
                log.info(f"Scraping weather data for: {self.year}-{self.month}")

                try:
                    if "unable to satisfy your request." not in soup.find('p').text:
                        for row in soup.find('table').find_all("tr")[1:-4]:
                            key = ""
                            daily_temp = {}

                            for item in row.find_all("th"):
                                if item.text.strip() and item.name == "th":
                                    key = f"{self.year}-{self.month}-{item.text.strip()}"

                            for index, item in enumerate(row.find_all("td")[0:3]):
                                conditions = ["Max", "Min", "Mean"]

                                if item.text.strip() and item.name == "td" and "LEGEND" not in item.text.upper():
                                    daily_temp[conditions[index]] = item.text.strip()
                                    self.weather[key] = daily_temp

                except Exception as e:
                    print("Error", e)
                    log.error("Error", e)

                self.check_for_previous_month(soup)

        except KeyboardInterrupt:
            session.close()
            print("Scrape aborted")
            log.warning("Scrape aborted")
        except Exception as e:
            print("Error:", e)
            log.error("Error:", e)

    def check_for_previous_month(self, soup):
        '''
        Checks if data for previous month is available.
        Will update the url and rerun the soup if true.
        '''
        try:
            address = soup.find(rel="prev", href=True)

            if address and not soup.find("li", {"class": "previous disabled"}):
                self.url = f'https://climate.weather.gc.ca{address.get("href")}'
                self.year = self.url[self.url.index("&Year=") + 6: self.url.index("&M")]
                self.month = self.url[self.url.index("Month=") + 6:]
                self.previous_month = True
                if(len(self.month) == 1):
                    self.month = "0" + self.month
            else:
                self.previous_month = False
        except Exception as e:
            print("Error", e)
            log.error("Error", e)

    def print_weather_data(self):
        '''Returns a string representation of the weather dictionary.'''
        try:
            log.info(self.weather)
            return print(self.weather)
        except Exception as e:
            print("Error:", e)
            log.error("Error:", e)

    def set_session(self):
        '''
        Creates a session to wrap request calls to account
        for request failures or request limits.
        '''
        try:
            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=1)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            return session
        except Exception as e:
            print("Error", e)
            log.error("Error", e)
