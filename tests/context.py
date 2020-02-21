import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(os.getcwd())

from source import source_html
from source import html_parser
from source import DwdData

from misc import ensure_correct_directory