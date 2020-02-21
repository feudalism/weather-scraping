from source import DwdData
from misc import ensure_correct_directory

ensure_correct_directory(__file__)	

WEATHER = {"path": './source-weather.html',
	"url": 'https://www.dwd.de/DE/wetter/wetterundklima_vorort/baden-wuerttemberg/stuttgart/_node.html'}
WARNING = {"path": './source-warning.html',
	"url": 'https://www.dwd.de/DE/wetter/warnungen_gemeinden/warnWetter_node.html?ort=Stuttgart'}

data = DwdData(region="Stuttgart",
	weather=WEATHER,
	warning=WARNING)
data.generate_soups()
data.parse()