from robot.libraries.BuiltIn import BuiltIn
from AppiumLibrary import AppiumLibrary
import base64
import time

class AdbUtils():
    def get_driver_instance(self):
        return BuiltIn().get_library_instance('AppiumLibrary')._current_application()

    def load_android_emulator_snapshot_using_adb(self,snapshot_name):
        driver = self.get_driver_instance()
        print(f"loading snapshot name : {snapshot_name}")
        command = f"avd snapshot load {snapshot_name}"
        driver.execute_script('mobile: execEmuConsoleCommand', {
        'command': command,
        'includeStderr': True,
        'timeout': 5000
        })
        time.sleep(5) #to wait for snapshot is completely loaded

    def list_android_emulator_snapshot_using_adb(self):
        driver = self.get_driver_instance()
        return driver.execute_script('mobile: execEmuConsoleCommand', {
        'command': 'avd snapshot list',
        'includeStderr': True,
        'timeout': 5000
        })

    def save_android_emulator_snapshot_using_adb(self,snapshot_name):
        driver = self.get_driver_instance()
        print(f"saving snapshot name : {snapshot_name}")
        command = f"avd snapshot save {snapshot_name}"
        driver.execute_script('mobile: execEmuConsoleCommand', {
        'command': command,
        'includeStderr': True,
        'timeout': 5000
        })
        time.sleep(5) #to wait for snapshot is completely loaded

    def disable_ime_keyboard_using_adb(self):
        driver = self.get_driver_instance()
        driver.execute_script('mobile: shell', {
        'command': 'ime',
        'args': ['disable', 'io.appium.settings/.AppiumIME' ],
        'includeStderr': True,
        'timeout': 5000
        })
        time.sleep(2)

    def enable_ime_keyboard_using_adb(self):
        driver = self.get_driver_instance()
        driver.execute_script('mobile: shell', {
        'command': 'ime',
        'args': ['enable', 'io.appium.settings/.AppiumIME' ],
        'includeStderr': True,
        'timeout': 5000
        })
        time.sleep(2)

    
    def press_search_button_on_appium_ime_using_adb(self):
        driver = self.get_driver_instance()
        driver.execute_script('mobile: shell', {
        'command': 'ime',
        'args': ['set', 'io.appium.settings/.UnicodeIME' ],
        'includeStderr': True,
        'timeout': 5000
        })
        time.sleep(2)
        driver.execute_script('mobile: shell', {
        'command': 'ime',
        'args': ['set', 'io.appium.settings/.AppiumIME' ],
        'includeStderr': True,
        'timeout': 5000
        })
        time.sleep(2)
        driver.execute_script('mobile: performEditorAction', {'action': 'search'})
