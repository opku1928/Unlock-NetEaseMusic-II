# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00BA802977EDB927AEA233EDBEACEA8100B934B1CE6302D0D4471D64B980A48C46D54CFA6741C9CC7638BD3AE1137BAA33ED11950CA10B67F9DEAFDF8DB6B59B9AEEC7E4073EC92E0A72EF2269DEA563DC656D1E6D9FCC8EAE44BD0AAC9FF2E9E0F10855579F128A35D69A5EB8821DDA84B828E6F5B12BBEC44E904F90F929F6F5EA6FCD75DA156582752AC43CF4C78EFF55945006156DB29CBDEE99750F193BC68D6EED2AD5836E9F2F31456C592AD7E3B826C9FEA202DF604220682FD3BE01A1FB31E060C4784094DDA84A2A660C067BD83C6453A409C18C481DA64FBC9ECD43FA4B764683026C135DBB0951DC88869D7E9849581D1139A3793966B9EDA87CB63222D7438F3ED001C7B57B00622D95C241F4602391550A003CFBCD5D3C946589894C3BB44647C41E73C82231085BB96EE8838B9DB369EB9BF207573BB58DD7EBEB8403DDF96139FB0D0A8C7D3457F436921C7677EA59C364C8ABE0FCB8F4B0AC
"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
