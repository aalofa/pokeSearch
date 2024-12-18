from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
import time,argparse,dotenv,os,pyautogui,datetime,pytz,ast
import seleniumUtil as SU

chrome_options = Options()
browser = webdriver.Chrome(options=chrome_options)

pokemonWithMove = set()
isMoveFound = False

def getMoveName():
    while not isMoveFound:
        move = input("Enter the EXACT name of the move you want to search for: ").replace(" ","-").strip().lower()
        browser.get(f'https://pokemondb.net/move/{move}')
        isMoveFound = True
        try:
            isMoveFound = SU.wait_for_element(browser,(By.CLASS_NAME,"infocard"),5)
        except:
            print(f"Move '{move}' not found. Please try again.")
            isMoveFound = False

getMoveName()
browser.maximize_window()
allPokemonElements = browser.find_elements(By.CLASS_NAME,"ent-name")

for pokemonElement in allPokemonElements:
    pokemonWithMove.add(pokemonElement.text)

print(pokemonWithMove)

browser.quit()
