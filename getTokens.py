from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import time


def tokenNames(driver):
    # Gets list of token names in BEP20 wallet exluding BNB
    table = driver.find_elements_by_xpath('//table[@class="table table-align-middle table-hover"]\
        //tbody//tr//td//div[@class="media-body"]//a[@class="hash-tag text-truncate font-weight-bold"]')
    cleanNames = []
    for token in table:
        token = token.text
        cleanNames.append(token)
    return cleanNames

def tokenNames_PP(driver, walletAdd):
    # Gets list of token names in BEP20 wallet and is used to ask user for 
    # purchase prices in GUI
    driver.get("https://bscscan.com/tokenholdings?a=" + walletAdd)
    time.sleep(0.5) #change to when page finished loading
    table = driver.find_elements_by_xpath('//table[@class="table table-align-middle table-hover"]\
        //tbody//tr//td//div[@class="media-body"]//a[@class="hash-tag text-truncate font-weight-bold"]')
    cleanNames = []
    for token in table:
        token = token.text
        cleanNames.append(token)
    return cleanNames


def tokenHoldingAmount(driver, tokenNames):
    # Get token holding amounts for each token in BEP20 wallet excluding BNB.
    # Token amounts begin at columns[11].text & increase by index of 8
    columns = driver.find_elements_by_xpath('//table[@class="table table-align-middle table-hover"]\
        //tbody//tr//td')
    tokenAmounts = []
    i = 11 # have to change the way this works 
    for token in tokenNames:
        tokenAmounts.append(columns[i].text)
        i = i + 8 
    return tokenAmounts


def tokenAddresses(driver):
    # Retrieve token addresses for pulling up Poocoin page for each token
    addresses = driver.find_elements_by_xpath('//table[@class="table table-align-middle table-hover"]\
        //tbody//tr//td//div[@class="media-body"]//a[@class="hash-tag text-truncate d-block font-size-1"]')
    return addresses


def tokenPrices(driver, addresses):
    # Use token addresses to loop thru Poocoin pages and extract price
    links =[]
    for add in addresses:
        links.append("https://poocoin.app/tokens/" + add.text)

    prices = []

    for link in links:
        driver.get(link)
        time.sleep(2) #change this to when page has finished loading
        price = driver.find_element_by_xpath('//div[@class="mb-1 d-flex flex-column lh-1"]//span')
        prices.append(price.text) #this will give only static list, might keep appending list if same instance of function is used?
    
    return prices




