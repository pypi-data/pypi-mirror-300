from ast import keyword
from datetime import datetime , timedelta,date
import html
from os import device_encoding
import time
import base64
from robot.api import logger
from robot.api.deco import keyword,not_keyword

class GeneralUtils():
    @keyword
    def decode_url(self,urls):
        list_of_link=[]
        for url in urls:
            decoded_url = html.unescape(url)
            print(decoded_url)
            list_of_link.append(decoded_url)
        return list_of_link
    
    @keyword
    def decode_base64(self,data_string):
        data_string_pad = data_string + "==="
        base64_bytes = data_string_pad.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes).decode('utf-8')
        return  message_bytes

    @keyword
    def check_value_in_file(self, old_list, new_list):
        for index,file in enumerate(new_list):
            if file in old_list:
                continue
            else:
                break
        return file



