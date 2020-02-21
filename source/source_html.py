import os, time, pickle

from misc import browser
from source import html_parser
	
def check_existing(path):
	if os.path.isfile(path):
		exists = True
		is_recent = check_existing_age(path)
	else:
		exists = False
		is_recent = False
	return exists, is_recent
		
def check_existing_age(path):
	def get_age(path):
		""" Returns age in hours """
		return (time.time() - os.stat(path).st_mtime ) / 3600.
		
	MAX_AGE = 1.
	SOURCE_HTML_AGE = get_age(path)
	if SOURCE_HTML_AGE <= MAX_AGE:
		return True
	else:
		return False

def get(exist_tuple, warning_url, path):
	exists, is_recent = exist_tuple
	
	if exists and is_recent:
		return get_existing(path)
	else:
		return get_new(warning_url, path)
	
def get_existing(path):
	with open(path, 'rb') as file:
		rawdata = pickle.Unpickler(file)
		rawdata = rawdata.load()
	return rawdata
	
def get_new(url, path):
	webdriver = browser.launch()
	webdriver.get(url) 
	
	time.sleep(2)
	source = html_parser.reduce(webdriver.page_source)
	save(source, path)
		
	webdriver.quit()
	return source
	
def save(source, path):
	with open(path, 'wb') as file:
		pickle.dump(source, file)

