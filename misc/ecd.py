import os

def ensure_correct_directory(file):
	INIT_DIR = os.getcwd()
	SCRIPT_DIR = os.path.dirname(os.path.realpath(file))
	if INIT_DIR != SCRIPT_DIR:
		os.chdir(SCRIPT_DIR)
	return INIT_DIR