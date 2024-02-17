import pyautogui as pag
import webbrowser as wb
import platform
import sounddevice as sd
import os

class Commands:
    def __init__(self):
        self.command_map = {
            0: "Open Browser",
            1: "Close Browser",
            2: "Minimize Window",
            3: "Maximize Window",
            4: "Open New Tab",
            5: "Scroll Up",
            6: "Scroll Down",
            7: "Left Click",
            8: "Right Click",
            9: "Mute/Unmute Microphone",
        }

    def open_browser(self):
        wb.open("https://www.google.com")

    def close_browser(self):
        pag.hotkey("ctrl","w")

    def minize_window(self):
        pag.hotkey("win","m")

    def maximize_window(self):
        pag.hotkey("win","up")

    def open_new_tab(self):
        pag.hotkey("ctrl","t")

    def scroll_up(self):
        pag.scroll(-100)

    def scroll_down(self):
        pag.scroll(100)

    def left_click(self):
        pag.click()

    def right_click(self):
        pag.click(button="right")

    def mute_unmute_microphone(self):
        if platform.system() == 'Windows':
            devices = sd.query_devices()
            mic_index = [i for i, device in enumerate(devices) if device['name'] == 'Microphone'][0]

            current_state = sd.query_devices()[mic_index]['muted']
            sd.query_devices()[mic_index]['muted'] = not current_state
        elif platform.system() == 'Linux':
            output = os.popen("amixer get Master unmute").read().strip()
            is_muted = output.split("[")[1].split("]")[0] == "off"

            os.system(f"amixer set Master {('unmute' if is_muted else 'mute')}")
        else:
            print("Microphone control support is not supported on this platform")

    def execute_commands(self,class_id):
        if 0 <= class_id < len(self.command_map):
            match class_id:
                case 0:
                    self.open_browser()
                case 1:
                    self.close_browser()
                case 2:
                    self.minize_window()
                case 3:
                    self.maximize_window()
                case 4:
                    self.open_new_tab()
                case 5:
                    self.scroll_up()
                case 6:
                    self.scroll_down()
                case 7:
                    self.left_click()
                case 8:
                    self.right_click()
                case 9:
                    self.mute_unmute_microphone()

