from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import seleniumUtil as SU
import json,time,math,os
from pokemonAttributes import PokemonAttribute

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
browser = webdriver.Chrome(options=chrome_options) #support Safari, Firefox

filteredPokemonSets:list[set] = []

cachedTypes : list[str] = []
cachedAbilities : list[str] = []
cachedMoves : list[str] = []

def loadCache():
    global cachedTypes
    global cachedAbilities
    global cachedMoves
    if os.path.exists("cache/cache.json"):
        with open("cache/cache.json","r+") as cacheFile:
            cache = json.load(cacheFile)
            cachedTypes = cache["types"]
            cachedAbilities = cache["abilities"]
            cachedMoves = cache["moves"]
            cacheFile.close()

def getFilteredPokemons(attribute: PokemonAttribute, attributeValue: str):
    pokemonWithMove = set()
    getAttributePage(attributeValue,attribute)
    allPokemonElements = browser.find_elements(By.CLASS_NAME,"ent-name")
    for pokemonElement in allPokemonElements:
        pokemonWithMove.add(pokemonElement.text)
    filteredPokemonSets.append(pokemonWithMove)
    print(f"Filter applied : has {attribute} -> {attributeValue}")


def verifyAttribute(attribute: PokemonAttribute, attributeValue: str):
    if attribute == PokemonAttribute.TYPE:
        return attributeValue in cachedTypes
    elif attribute == PokemonAttribute.ABILITY:
        return attributeValue in cachedAbilities
    elif attribute == PokemonAttribute.MOVE:
        return attributeValue in cachedMoves
    else:
        return False
    
def getAttributePage(attributeName: str, attribute: PokemonAttribute):
    isAttributeFound = False
    while not isAttributeFound:
        browser.get(f'https://pokemondb.net/{attribute}/{attributeName.replace(" ","-")}')
        isAttributeFound = True
        try:
            isAttributeFound = SU.wait_for_element(browser,(By.CLASS_NAME,"ent-name"),2)
        except:
            print(f"{attribute} '{attributeName}' not found. Please try again.")
            isAttributeFound = False

def filterOutTypeAbbreviation(types : set):
    typesCopy = types.copy()
    for _type in types:
        if len(_type) <= 3 and _type != "BUG" and _type != "ICE":
            typesCopy.remove(_type)
    return typesCopy

def getAllFromAttribute(path: str,className: str):
    attributes = set()
    browser.get(f'https://pokemondb.net/{path}')
    allPokemonElements = browser.find_elements(By.CLASS_NAME,className)
    for pokemonElement in allPokemonElements:
        attributes.add(pokemonElement.text)
    if path == "type":
        attributes = filterOutTypeAbbreviation(attributes)
    return sorted(attributes)

def updateCache():
    if getCacheValidity() == False:
        global cachedTypes
        global cachedAbilities
        global cachedMoves
        cache = {"timestamp": math.floor(time.time()), "types": cachedTypes, "abilities": cachedAbilities, "moves": cachedMoves}
        jsonData = json.dumps(cache, indent=4)
        with open("cache/cache.json","w") as cacheFile:
            cacheFile.write(jsonData)
            cacheFile.close()
    else:
        print("Cache not updated; cache is still fresh.")

def getAllTypes():
    global cachedTypes
    types = getAllFromAttribute("type","type-icon")
    cachedTypes = types
    updateCache()

def getAllAbilities():
    global cachedAbilities
    abilities = getAllFromAttribute("ability","ent-name")
    cachedAbilities = abilities
    updateCache()

def getAllMoves():
    global cachedMoves
    moves = getAllFromAttribute("move/all","ent-name")
    cachedMoves = moves
    updateCache()

def getCacheValidity():
    if os.path.exists("cache/cache.json"):
        with open("cache/cache.json","r") as cacheFile:
            cache = json.load(cacheFile)
            cacheFile.close()
            return math.floor(time.time()) - cache["timestamp"] >= 86400
    return False


# loadCache()

# getAllMoves()
# getAllAbilities()
# getAllTypes()

browser.quit()
