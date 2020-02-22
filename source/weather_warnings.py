from bs4 import BeautifulSoup

def parse(soup):
	info = get_warning(soup)
	
	warning_title = get_title(info)
	warning_date = get_date(info)
	warning_text = get_text(info)
	warning_extra = get_extra(info)
	
	return "\n".join([warning_title,
			warning_date,
			warning_text,
			warning_extra])
		
def check(soup):		
	no_headline = soup.find("div", class_="noWarningHeadline")		
	if no_headline:
		return False
	else:
		return True
	
def get_warning(soup):
	warning = soup.find("div", class_="warningDetailsBox")
	return warning
	
def get_title(info):
	return info.find("h3").text
	
def get_date(info):
	return info.find("strong").text
	
def get_text(info):
	return info.find("div", class_="").text
	
def get_extra(info):
	return info.find("p", class_="instructionTextClosed").text


