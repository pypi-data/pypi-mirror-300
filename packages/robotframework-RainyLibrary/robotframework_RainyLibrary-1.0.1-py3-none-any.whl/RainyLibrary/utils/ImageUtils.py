import re
import cv2
import numpy as np
from robot.api.deco import keyword,not_keyword
from robot.api import logger
from datetime import datetime, timezone, timedelta,date
tz = timezone(timedelta(hours = 7))

class ImageUtils():
    @not_keyword
    def _check_image_and_return_xy(self,expected,screenshot,threshold):
        image           = cv2.imread(screenshot)
        template        = cv2.imread(expected)
        #convert to gray color first, since cv2 operate better on gray color 
        image_gray      = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        template_gray   = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)

        result              = cv2.matchTemplate(image_gray,template_gray,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        match_indices       = np.arange(result.size)[(result>threshold).flatten()]
        result_confident    = np.unravel_index(match_indices,result.shape)
        H, W                = template_gray.shape
        try:
            x = result_confident[0].max()
            y = result_confident[1].max()
            top_left = (x, y)
            middle_image = (x + int(W/2), y + int(H/2))
            middle_image_xy = []
            for item in middle_image:
                middle_image_xy.append(item)
            print(middle_image_xy)
            print(top_left)
            return True,middle_image_xy
        except:
            err_msg = f"Unable to find expected image on screen with threshold {threshold}"
            return False,err_msg
    
    @keyword
    def image_should_be_visible_on_screen(self,expected,screenshot,threshold):
        is_found_image,xy = self._check_image_and_return_xy(expected,screenshot,threshold)
        return is_found_image,xy