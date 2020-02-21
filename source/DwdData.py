from bs4 import BeautifulSoup

from source import source_html
from source import html_parser
from source import weather_warnings as wwarn
from source import weather_data as wdata

class DwdData(object):
	def __init__(self, region, weather=None, warning=None):
		self.region = region
		self.is_warning = None
		self.weather = weather
		self.warning = warning
		
	def parse(self, do_print=True):		
		if do_print:
			print(f"{self.region}\n")
			self.parse_weather(self.weather["soup"])
			self.parse_warning(self.warning["soup"])
		
	def generate_soups(self):
		for rubric in [self.weather, self.warning]:
			exists = source_html.check_existing(rubric["path"])	
			rawdata = source_html.get(exists, rubric["url"], rubric["path"])
			rubric["soup"] = html_parser.get_soup(rawdata)
			
	def parse_weather(self, soup):
		wdata.parse(soup)
		print()

	def parse_warning(self, soup, do_print=True):
		self.is_warning = wwarn.check(soup)
		if self.is_warning and do_print:
			wwarn.parse(soup)
			print()
			