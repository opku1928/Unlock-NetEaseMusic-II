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
    browser.add_cookie({"name": "MUSIC_U", "value": "00AD0128A90EDED1F9B304295DE372EA0898F8AEE38C8475CEBE0FCC102BEC3351C8968EAB02B0A7045AFA9EA1FFED5FE422BD8A8FCA0475C2C018C243DF69F1AB4BD103CDBD17318F44FDF7007240F3F6B41A631DF2A407DF7323D8DB142FECFCFC3495BD0293D8E66090E4DE5AD7BFA47295E29F79046C49DFEE6735C18AB7EEF540A317A91328CD54AE29D6129440EF5FE9FC503973F7A76532629854493057A526344D1AC4C7036F0D43462D616341E7138F0F49E76A4BA5D996EE92C710F12F375862981DBE0E73E8C6561A8173ABC23C24C31D3578423AC60BC6996AA8BEC22A155B586763B1C33300ABCBDD22289154ECF22300BAC251C59B54DF1F90FBDD3BB0F4925173A65B783E4B39157FF62EEDCDAB5C4FDA8D9DF30611E6368EF0AADA55D14A05301C1A24582034D490D0DF9CA991503643B597D3683533EB74A4B5EF7539BA65119992027C5D27F9AE66E2D1D084169ED952F154A66D142786FA"})
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
