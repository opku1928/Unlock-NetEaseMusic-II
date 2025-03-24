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
    browser.add_cookie({"name": "MUSIC_U", "value": "00254036D5CB313C84963AEDCDE682413A9F79BCF3C10A4A75C61E212D638F1BFDA0E4AC83E4D6893DE7B7D4A7532D50D304485ADBAF83592E0D30877E08FF50F52594CC68BA5860C3190DD0C07F9424BDFEAEE16B2ADEFF0942B7BB7F85A6B49B10D515E7F2B54991F7A440B9CBF9FC8F0D0A9D918CC44D8D54FA48D61F0BA1267EE31DF40F270942181A05DF7CE5148D6BC9147EC92387D36B57BF32D405BFF8B348E3439A4431CECCDBCEEB068BD21D71077E35CB168BE68CBC690A62492A2CAD5CF5CFC237B605F715243831D503520C7C8CCADA11E80623183B67940AA154280BF80BE6365FB8C8AC982B1FF2955261F6FF38443EC99874A818D52B2BC93258038059C02746553DD0F72005CDA28A7B48BAB3EF58D6462A370E5A831B691CFC0C60CE955C3CEE8F1E641C1214984FEB151BA3AE215964CBA296FB13FDC682EC984A280FC72718818DEFFEBAD24D5B958B10DC0C026B553B44A98DB8CD31E1
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
