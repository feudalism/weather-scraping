from bs4 import BeautifulSoup
			
def parse(soup):
	info = soup.find("div", {"id": "wetklitab"} )		
	table = info.find("tbody").find_all("tr")
	
	table_picture = table[1]
	weather = get_weather(table_picture)
	print(weather)
	
	data_headers = ["Temperature", "Humidity", "Wind speed", "Air pressure"]
	max_header_length = len(max(data_headers, key=len))
	
	for i, header in enumerate(data_headers):
		table_data = table[i + 2]
		data = get_tr_data(table_data)
		
		header = header.ljust(max_header_length + 1)
		print(f"{header}: {data}")
	
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