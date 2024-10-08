from robot.libraries.BuiltIn import BuiltIn
from AppiumLibrary import AppiumLibrary
import base64


class AppiumUtils():
    def get_driver_instance(self):
        return BuiltIn().get_library_instance('AppiumLibrary')._current_application()

    def push_image_file_to_emulator(self,android_path,path_file):
        driver = self.get_driver_instance()
        dest_path = android_path
        data = {}
        with open(path_file, 'rb') as f: # open the file in read binary mode
            image = base64.b64encode(f.read())
            image_str = image.decode()
        return driver.push_file(dest_path, image_str)