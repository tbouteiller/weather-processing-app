from scrape_weather import WeatherScraper
from db_operations import DbOperations

test = WeatherScraper()
db = DbOperations()

test.scrape()
db.initalize_db()
db.fetch_data(test.weather)
