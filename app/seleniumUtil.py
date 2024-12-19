from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
import time,argparse,dotenv,os,pyautogui,datetime,pytz,ast
defaultDelay = 10

def wait_for_element(browser,selector: tuple[By, str], delay: int = defaultDelay) -> WebElement:
    return WebDriverWait(browser, delay).until(EC.presence_of_element_located(selector))