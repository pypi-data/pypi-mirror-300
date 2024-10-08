from ast import keyword
from curses import keyname
import os.path
import json
from robot.api import logger
from robot.api.deco import keyword,not_keyword

class JsonUtils():
    @keyword
    def load_json_from_file_with_utf8(self,file_path):
        logger.debug("Check if file exists")
        if os.path.isfile(file_path) is False:
            logger.error("JSON file: " + file_path + " not found")
            raise IOError
        with open(file_path,encoding="utf8") as json_file:
            data = json.load(json_file)
        return data