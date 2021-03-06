import unittest
import os, time
from shutil import copy, move

from context import DwdData
from context import source_html, html_parser
from context import ensure_correct_directory
from context import WidgetGallery
	
def addtests(suite, class_):
	tests = [class_(k) for k in class_.__dict__ if 'test' in k]
	suite.addTests(tests)

class TestDWDENewHTML(unittest.TestCase):	
	@classmethod
	def setUpClass(self):
		self.warning_path = './source.html'
	
	def test_check_for_existing_source_html(self):
		exists, _ = source_html.check_existing(self.warning_path)
		self.assertFalse(exists)
		
	def test_get_rawdata(self):
		exist_tuple = (False, False)
		rawdata = source_html.get(exist_tuple,
			warning_url='https://www.dwd.de/DE/wetter/warnungen_gemeinden/warnWetter_node.html?ort=Stuttgart',
			path=self.warning_path)
		self.assertIsNotNone(rawdata)
		
	@classmethod
	def tearDownClass(self):
		if os.path.isfile(self.warning_path):
			copy(self.warning_path, './source-debug-copy.html')
			os.remove(self.warning_path)
		
class TestDWDExistingHTML(unittest.TestCase):
	@classmethod
	def setUpClass(self, weather_path, warning_path, region):
		WEATHER = {"path": weather_path,
			"url": "https://www.dwd.de/DE/wetter/wetterundklima_vorort/baden-wuerttemberg/stuttgart/_node.html"}
		WARNING = {"path": warning_path, "url": ""}
		
		self.reset_data_age(self, WEATHER["path"])
		self.reset_data_age(self, WARNING["path"])
		
		self.data = DwdData(region=region, weather=WEATHER, warning=WARNING)
		self.data.generate_soups()
		
	def reset_data_age(self, path):
		filename = os.path.basename(path)
		copy(filename, filename + "copy")
		move(filename + "copy", filename)
		
	def test_parse(self):
		self.data.parse(do_print=False)
		
	def test_check_soups(self):
		for rubric in [self.data.weather, self.data.warning]:
			self.assertIsNotNone(rubric["soup"])
		
	def test_check_for_existing_source_html(self):
		for rubric in [self.data.weather, self.data.warning]:
			exists, _ = source_html.check_existing(rubric["path"])
			self.assertTrue(exists)
		
	def check_if_warning(self):
		self.data.parse_warning(self.data.warning["soup"])		
		self.assertIsNotNone(self.data.is_warning)
		
class TestDWDExistingHTMLWithWarning(TestDWDExistingHTML):
	@classmethod
	def setUpClass(self):
		super().setUpClass(
			weather_path='./w_warn-weather.html',
			warning_path='./w_warn-warning.html',
			region="Stuttgart")
		
	def test_parse(self):
		super().test_parse()
		
	def test_check_soups(self):
		super().test_check_soups()
		
	def test_check_for_existing_source_html(self):
		super().test_check_for_existing_source_html()
		
	def test_check_if_warning(self):
		super().check_if_warning()
		self.assertTrue(self.data.is_warning)
		
class TestDWDExistingHTMLWithoutWarning(TestDWDExistingHTML):
	@classmethod
	def setUpClass(self):
		super().setUpClass(
			weather_path='./wo_warn-weather.html',
			warning_path='./wo_warn-warning.html',
			region="Düsseldorf")
		
	def test_parse(self):
		super().test_parse()
		
	def test_check_soups(self):
		super().test_check_soups()
		
	def test_check_for_existing_source_html(self):
		super().test_check_for_existing_source_html()
		
	def test_check_if_warning(self):
		super().check_if_warning()	
		self.assertFalse(self.data.is_warning)

class TestGUINotRefreshable(TestDWDExistingHTMLWithWarning):
	@classmethod
	def setUpClass(self):
		super().setUpClass()
		self.data.parse_warning(self.data.warning["soup"])
		self.weather_data, self.warning_data = self.data.parse(do_print=False)
		self.refreshable = False
		
	def test_check_soups(self):
		super().test_check_soups()
		
	def test_check_if_warning(self):
		super().test_check_if_warning()
		
	def test_gui(self):
		WidgetGallery(self.data.region,
			self.weather_data, self.warning_data, data=self.data,
			refreshable=self.refreshable)
		
class TestGUIRefreshable(TestGUINotRefreshable):
	@classmethod
	def setUpClass(self):
		super().setUpClass()
		self.refreshable = True
		
		self.old_weather_path = self.data.weather["path"] 
		self.new_weather_path = self.get_new_weather_path(self)
		self.reset_data_age(self, self.new_weather_path)
		
		copy(self.old_weather_path, self.old_weather_path + "copy")
		
	def get_new_weather_path(self):
		oldpath = self.old_weather_path
		
		split = os.path.splitext(oldpath)
		oldname = split[0]
		ext = split[1]
		
		return oldname + "-new" + ext
		
	def test_refresh_data(self):
		WidgetGallery(self.data.region,
			self.weather_data, self.warning_data, data=self.data,
			refreshable=self.refreshable, debug=True)
			
	@classmethod
	def tearDownClass(self):
		move(self.old_weather_path + "copy", self.old_weather_path)
		
		
if __name__ == '__main__':
	ensure_correct_directory(__file__)
	# unittest.main()
	
	suite = unittest.TestSuite()
	# addtests(suite, TestDWDENewHTML)
	# addtests(suite, TestDWDExistingHTMLWithWarning)
	# addtests(suite, TestDWDExistingHTMLWithoutWarning)
	# addtests(suite, TestGUINotRefreshable)
	addtests(suite, TestGUIRefreshable)
	
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)