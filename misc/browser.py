from selenium import webdriver
from selenium.webdriver.firefox.options import Options
	
def launch():
	print("Launching browser...")
	USER_AGENT = {"User-agent":"Mozilla on Windows, Python"}

	options = Options()
	options.headless = True
	WEBDRIVER = webdriver.Firefox(options=options,
			executable_path=r'C:\Users\user3\Downloads\geckodriver.exe')
	
	return WEBDRIVER