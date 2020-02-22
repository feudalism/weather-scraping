from bs4 import BeautifulSoup

from source import source_html
from source import html_parser
from source import weather_warnings as wwarn
from source import weather_data as wdata

from source.weather_data import DATA_HEADERS

class DwdData(object):
	def __init__(self, region, weather=None, warning=None):
		self.region = region
		self.is_warning = None
		self.weather = weather
		self.warning = warning
		
	def print_to_console(self, do_print=True):
		pass
		
	def print_weather_data(self, data):
		max_header_length = len(max(DATA_HEADERS, key=len))
		for k,v in data.items():
			key = k.ljust(max_header_length + 1)
			print(f"{key}: {v}")
		
	def parse(self, do_print=True):	
		weather_data = self.parse_weather(self.weather["soup"])	
		warning_text = self.parse_warning(self.warning["soup"])
		
		if do_print:
			print(f"{self.region}\n")
			self.print_weather_data(weather_data)
			print(f"{warning_text}\n")
			
		return weather_data, warning_text	
		
	def generate_soups(self):
		for rubric in [self.weather, self.warning]:
			exists = source_html.check_existing(rubric["path"])	
			
			rawdata = source_html.get(exists, rubric["url"], rubric["path"])
			rubric["soup"] = html_parser.get_soup(rawdata)
			
	def parse_weather(self, soup):
		return wdata.parse(soup)

	def parse_warning(self, soup):
		self.is_warning = wwarn.check(soup)
		if self.is_warning:
			return wwarn.parse(soup)
		else:
			return ""
			