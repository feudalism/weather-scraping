from bs4 import BeautifulSoup
	
def get_soup(rawdata):
	return BeautifulSoup(rawdata, 'lxml')
	
def reduce(source):
	temp_soup = get_soup(source)
	info_soup = temp_soup.find("section", class_="content")
	# info_soup = temp_soup.find("div", {"id": "infoBox"} )
	
	assert info_soup is not None
	assert info_soup != ""
	
	return str(info_soup)