from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import os
	
class WidgetGallery(object):
	def __init__(self, region, weather_data, warning_data, data=None,
			refreshable=True, debug=False):
		self.region = region
		self.weather_data = weather_data
		self.warn_data = warning_data
		self.data = data
		self.debug = debug
		
		self.app = QApplication([])
		self.refreshable = refreshable
		self.window = QWidget()		
		self.main_layout = QVBoxLayout(self.window)
		self.wdl = QVBoxLayout()
	
		self.set_layout()
		self.run_app()
		
	def formatting(self, label):
		font = QFont()
		font.setBold(True)
		font.setPointSize(10)
		label.setFont(font)
		
	def on_refresh(self):
		assert self.data is not None
		
		if self.debug:
			self.data.weather["path"] = "w_warn-weather-new.html"
		else:
			os.remove(self.data.weather["path"])
			os.remove(self.data.warning["path"])
		
		self.data.generate_soups()
		self.weather_data, self.warn_data = self.data.parse(do_print=False)
		
		self.update_weather_data_layout()
		
	def update_weather_data_layout(self):
		self.clear_layout(self.wdl)
		self.weather_data_layout()
		
	def clear_layout(self, layout):
		while layout.count():
			sublayout = layout.takeAt(0)
			
			while sublayout.count():
				child = sublayout.takeAt(0)
				child.widget().deleteLater()
			  
	def refresh_layout(self):
		if self.refreshable:
			refresh_button = QPushButton("Refresh")
			refresh_button.setFixedWidth(refresh_button.sizeHint().width())
			refresh_button.setDefault(False)
			refresh_button.clicked.connect(lambda : self.on_refresh())
			
			self.main_layout.addWidget(refresh_button, alignment=Qt.AlignRight)
	
	def region_layout(self):
		region_label = QLabel(self.region)
		self.formatting(region_label)
		self.main_layout.addWidget(region_label)
	
	def weather_data_layout(self):
		layout = self.wdl
		
		for k, v in self.weather_data.items():
			sl = self.weather_data_sublayout(k,v)
			layout.addLayout(sl)
			
		if layout.parent() is None:
			self.main_layout.addLayout(layout)
			
		self.wdl = layout
		
	def weather_data_sublayout(self, k,v):
		layout = QHBoxLayout()
		
		hdr_label = QLabel(k)
		data_label = QLabel(v)
		
		layout.addWidget(hdr_label)
		layout.addWidget(data_label)
		
		return layout
		
	def warning_layout(self):
		if self.warn_data is not None and self.warn_data != "":
			layout = QVBoxLayout()
			
			warning_hdr_label = QLabel("Warnings")
			self.formatting(warning_hdr_label)
			warning_label = QLabel(self.warn_data, wordWrap=True)
			
			layout.addWidget(warning_hdr_label)
			layout.addWidget(warning_label)
			
			self.main_layout.addLayout(layout)
		
	def set_layout(self):	
		self.refresh_layout()
		self.region_layout()
		self.weather_data_layout()
		self.warning_layout()
		
	def run_app(self):
		self.window.setFixedWidth(300)
		self.window.show()
		self.app.exec_()

