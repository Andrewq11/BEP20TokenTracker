from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from getTokens import tokenNames, tokenHoldingAmount, tokenAddresses, tokenPrices
import PySimpleGUI as sg
import time

# Hello Andre, you're a goober.
# Settings for font in GUI and selenium webdriver
fnt = "Arial 11 underline"
prox = Proxy()
prox.http_proxy = "51.158.123.35:9999"
capabilities = webdriver.DesiredCapabilities.CHROME
prox.add_to_capabilities(capabilities)

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--log-level=3")
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH, options=options,desired_capabilities=\
                            capabilities)


# Input the BEP20 wallet address you want to collect token info on.
walletAddress = "0xadf589678611e28a4302549d8d6e28ae3c822ecd"
driver.get("https://bscscan.com/tokenholdings?a=" + walletAddress)
time.sleep(0.5)


# Functions get list of tokens in wallet, amounts of each token, contract 
# addresses for token, and prices of each token via Poocoin
table = tokenNames(driver)
tokenAmounts = tokenHoldingAmount(driver, table)
address = tokenAddresses(driver)
prices = tokenPrices(driver, address)


# Converts price and token amount string into clean floats for calculations
cleanPrices = []
for price in prices:
    price = price.replace('$', '')
    price = float(price)
    cleanPrices.append(price)

cleanAmounts = []
for amount in tokenAmounts:
    amount = amount.replace(',', '')
    amount = float(amount)
    cleanAmounts.append(amount)


# Input price by order of row excluding BNB (2nd row is [0])
# Add purchase prices manually, calculates P/L and value for tokens that DO NOT 
# have 0 for purchase price.
# Put 0 for purchase price if wallet has negligible balance for it and
# don't want PL or value calculated.
purchasePrices = []
PurchasePrice0 = 0.000000324
PurchasePrice1 = 0.00000000673
PurchasePrice2 = 0
PurchasePrice3 = 0.000000145
PurchasePrice4 = 0.00000006324
PurchasePrice5 = 0
PurchasePrice6 = 0

purchasePrices.append(PurchasePrice0)
purchasePrices.append(PurchasePrice1)
purchasePrices.append(PurchasePrice2)
purchasePrices.append(PurchasePrice3)
purchasePrices.append(PurchasePrice4)
purchasePrices.append(PurchasePrice5)
purchasePrices.append(PurchasePrice6)


# Calculating PL for tokens with non-zero purchase price
pLGain = []
i = 0
for p in purchasePrices:
    if p == 0:
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
    val = "$" + str(val)
    values.append(val)
    i = i + 1
totalValue = round(sum(totalVals), 2)


# Generating columns for the GUI
tokenColumn = [[sg.Text("Token", font=fnt)]]
for token in table:
    tokenColumn.append([sg.Text(token)])

amountColumn = [[sg.Text("Amount", font=fnt)]]
for amount in tokenAmounts:
    amountColumn.append([sg.Text(amount)])

priceColumn = [[sg.Text("Price", font=fnt)]]
for price in cleanPrices:
    priceColumn.append([sg.Text(price)])

pLColumn = [[sg.Text("P/L", font=fnt)]]
for pl in pLGain:
    pLColumn.append([sg.Text(pl)])

valColumn = [[sg.Text("Value (USD)", font=fnt)]]
for val in values:
    valColumn.append([sg.Text(val)])

totColumn = [[sg.Text("= $" + str(totalValue))]]


# Layout for GUI w/ columns
layout = [
    [sg.Frame(layout=tokenColumn, title=''), sg.Frame(layout=amountColumn, title=''),\
     sg.Frame(layout=priceColumn, title=''), sg.Frame(layout=pLColumn, title=''),
         sg.Frame(layout=valColumn, title='')],
    [sg.Sizer(434,10), sg.Frame(layout=totColumn, title='')],
    [sg.Sizer(375,10), sg.Button("Update Prices", pad=(5,12)), sg.Button("Close", pad=(5,12))]
    ]

# Launches GUI in loop w/ above layout
window = sg.Window("Defi Token Tracker", layout, margins=(100,100), icon=r"C:\Users\andre\Downloads\favicon.ico")
while True: 
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Close":
        break

window.close()

