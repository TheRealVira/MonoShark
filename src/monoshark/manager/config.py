"""Config Manager just managing se configs."""
from configparser import ConfigParser

CONFIG = ConfigParser(interpolation=None)
CONFIG.read("config.ini")
