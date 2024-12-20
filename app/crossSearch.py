from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import seleniumUtil as SU
from pokemonAttributes import PokemonAttribute

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
browser = webdriver.Chrome(options=chrome_options)

filteredPokemonSets:list[set] = [] #TODO: list[tuple[set,operation]] to allow the user to choose the operation (intersection, union);

def getFilteredPokemons(attribute: PokemonAttribute, attributeValue: str):
    pokemonWithMove = set()
    getAttributePage(attributeValue,attribute)
    allPokemonElements = browser.find_elements(By.CLASS_NAME,"ent-name")
    for pokemonElement in allPokemonElements:
        pokemonWithMove.add(pokemonElement.text)
    filteredPokemonSets.append(pokemonWithMove) #TODO: allow the user to choose the operation (intersection, union);
    

def getAttributePage(attributeName: str, attribute: PokemonAttribute):
    isAttributeFound = False
    while not isAttributeFound:
        browser.get(f'https://pokemondb.net/{attribute}/{attributeName}')
        isAttributeFound = True
        try:
            isAttributeFound = SU.wait_for_element(browser,(By.CLASS_NAME,"ent-name"),5)
        except:
            print(f"{attribute} '{attributeName}' not found. Please try again.")
            isAttributeFound = False

getFilteredPokemons(PokemonAttribute.MOVE,"flamethrower")
getFilteredPokemons(PokemonAttribute.ABILITY,"sturdy")
getFilteredPokemons(PokemonAttribute.TYPE,"ground")
getFilteredPokemons(PokemonAttribute.TYPE,"rock")

filteredPokemonSet = set.intersection(*filteredPokemonSets)

print(f"Filtered pokemons :  {filteredPokemonSet}")


browser.quit()
