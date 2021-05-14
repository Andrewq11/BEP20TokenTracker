from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import PySimpleGUI as sg
import time

fnt = "Arial 11 underline"


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
    time.sleep(0.5)
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
    i = 11
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
    j = 0
    for link in links:
        driver.get(link)
        time.sleep(1.4)
        price = driver.find_element_by_xpath('//div[@class="mb-1 d-flex flex-column lh-1"]//span')
        prices.append(price.text)
    
    return prices


def existingLoad(driver, walletAdd, pPrices):
    # Function loads all token data and displays in GUI
    # Takes three arguments being driver, BEP20 wallet address andlist of token purchase prices
    driver.get("https://bscscan.com/tokenholdings?a=" + walletAdd)
    time.sleep(0.5)

    table = tokenNames(driver)
    tokenAmounts = tokenHoldingAmount(driver, table)
    address = tokenAddresses(driver)
    print("Current prices:")
    prices = tokenPrices(driver, address)
    print(prices)

    cleanPrices = []
    for price in prices:
        price = price.replace('$', '')
        price = price.replace(',', '')
        print(price)
        price = float(price)
        cleanPrices.append(price)

    cleanAmounts = []
    for amount in tokenAmounts:
        amount = amount.replace(',', '')
        amount = float(amount)
        cleanAmounts.append(amount)

    purchasePrices = []
    for purchaseP in pPrices:
        purchasePrices.append(purchaseP)


    # Calculating PL for tokens w/ non-zero and non-one purchase prices
    pLGain = []
    i = 0
    for p in purchasePrices:
        if p == 0 or p == 1:
            i = i + 1
            p = '---'
            pLGain.append(p)
            continue
        p = round(((cleanPrices[i] - p) / p) * 100, 2)
        p = str(p) + "%"
        pLGain.append(p)
        i = i + 1

    # Calculating value of token holding for non-zero purchase prices
    values = []
    totalVals = []
    i = 0
    for v in purchasePrices:
        if purchasePrices[i] == 0:
            i = i + 1
            val = '---'
            values.append(val)
            continue
        val = round(cleanPrices[i] * cleanAmounts[i], 2)
        totalVals.append(val)
        val = "{:,}".format(val)
        val = "$" + str(val)
        values.append(val)
        i = i + 1
    totalValue = round(sum(totalVals), 2)
    totalValue = "{:,}".format(totalValue)


    # Generating columns for the GUI
    tokenColumn = [[sg.Text("Token", font=fnt)]]
    i = 0
    for token in table:
        if totalVals[i] >= 25:
            tokenColumn.append([sg.Text(token)])
            i = i + 1
            print('added')
        else:
            i = i + 1
            print('skipped')

    i = 0
    amountColumn = [[sg.Text("Amount", font=fnt)]]
    for amount in tokenAmounts:
        if totalVals[i] >= 25:
            amountColumn.append([sg.Text(amount)])
            i = i + 1
        else: 
            i = i + 1

    i = 0
    priceColumn = [[sg.Text("Price", font=fnt)]]
    for price in cleanPrices:
        if totalVals[i] >= 25:
            priceColumn.append([sg.Text(price)])
            i = i + 1
        else: 
            i = i + 1

    i = 0
    pLColumn = [[sg.Text("P/L", font=fnt)]]
    for pl in pLGain:
        if totalVals[i] >= 25:
            pLColumn.append([sg.Text(pl)])
            i = i + 1
        else:
            i = i + 1

    i = 0
    valColumn = [[sg.Text("Value (USD)", font=fnt)]]
    for val in values:
        if totalVals[i] >= 25:
            valColumn.append([sg.Text(val)])
            i = i + 1
        else:
            i = i + 1

    totColumn = [[sg.Text("= $" + str(totalValue))]]

    # Layout for GUI w/ each column
    layout = [
    [sg.Text('Wallet Address: ' + walletAdd, pad=(10,10))],    
    [sg.Frame(layout=tokenColumn, title=''), sg.Frame(layout=amountColumn, title=''),\
    sg.Frame(layout=priceColumn, title=''), sg.Frame(layout=pLColumn, title=''),
        sg.Frame(layout=valColumn, title='')],
    [sg.Sizer(402,10), sg.Frame(layout=totColumn, title='')],
    [sg.Button('Back', pad=(5,12)), sg.Sizer(323,10), sg.Button("Update Prices", pad=(5,12)),\
         sg.Button("Close", pad=(5,12))]
    ]

    return layout

