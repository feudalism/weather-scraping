from bs4 import BeautifulSoup

DATA_HEADERS = ["Weather", "Temperature", "Humidity", "Wind speed", "Air pressure"]
			
def parse(soup):
	info = soup.find("div", {"id": "wetklitab"} )		
	table = info.find("tbody").find_all("tr")
	
	data = dict.fromkeys(DATA_HEADERS)
	
	for i, header in enumerate(DATA_HEADERS):			
		table_data = table[i + 1]
		
		if header == "Weather":
			data[header] = get_weather(table_data)
		else:
			data[header] = get_tr_data(table_data)
		
	return data
	
def get_weather(info):
	current_weather_pic = info.find("img")['src']
	
	def translate_pic(pic):
		PIC_DICT = {"/DE/wetter/_functions/piktos/pic_5-8.png?__blob=normal": "A bit cloudy",
			"/DE/wetter/_functions/piktos/pic_2-8.png?__blob=normal": "Slightly cloudy",
			"/DE/wetter/_functions/piktos/pic_61.png?__blob=normal": "Rain"}
		return PIC_DICT.get(pic, pic)
		
	return translate_pic(current_weather_pic)
	
def get_tr_data(info):
	return info.find_all("td")[1].text