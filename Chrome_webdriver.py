from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class My_Webdriver:
    def __init__(self):
        print("Opening Browser...")
    def set_options(self):
        chrome_op=Options()
        #Download info setting
        self.download_path='D:\\Desktop'
        prefs = {"download.directory_upgrade": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.enabled": False,
                "download.prompt_for_download": False,
                'profile.default_content_settings.popups': 0,
                'download.default_directory': self.download_path+"\\"}
        chrome_op.add_experimental_option('prefs',prefs)
        #Set window size
        chrome_op.add_argument('--window-size=1920,1080')
        #
        chrome_op.add_argument('--start-maximized')
        #Remove console message
        chrome_op.add_argument('--log-level=3')
        #Open chrome headless
        chrome_op.add_argument('--headless')
        chrome_op.add_argument('--disable-gpu')
        #Open driver
        try:
            self.Chrome_browser=webdriver.Chrome(chrome_options=chrome_op) #executable_path is default
        except:
            print("====================================")
            print(" Please update the Chrome Webdriver")
            print("====================================")
            input()
        #driver=webdriver.Chrome() #--original chrome opening
        return self.Chrome_browser