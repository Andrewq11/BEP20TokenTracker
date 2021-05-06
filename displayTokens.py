from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from getTokens import tokenNames, tokenHoldingAmount, tokenAddresses, tokenPrices, tokenNames_PP, existingLoad
import PySimpleGUI as sg
import pickle
import time

# Settings for font in GUI and selenium webdriver
fnt = "Arial 11 underline"
prox = Proxy()
prox.http_proxy = "51.158.123.35:9999"
capabilities = webdriver.DesiredCapabilities.CHROME
prox.add_to_capabilities(capabilities)

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--log-level=3")
PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH, options=options,desired_capabilities=\
                            capabilities)


# Function which starts program. Will first check if program has a wallet 
# address stored and if does, will then check for purchase prices of each token
# in BEP20 wallet. 
# If there is no wallet address stored in program from prior use, program will
# ask for wallet address and proceed to purchasePriceScreen.
def inputAddress():
    layout = [[sg.Text('Enter your BEP20 Wallet Address')],
    [sg.InputText(size=(42,20))],
    [sg.Sizer(185,0), sg.Button('Continue'), sg.Button("Close", pad=(5,12))]
    ]

    window = sg.Window("BEP20 Token Tracker", layout, margins=(50,50), icon=r"C:\Users\andre\Downloads\favicon.ico")
    while True: 
        try:
            infile = open("localInfo.pickle", "rb")
            infileP = open("pPrices.pickle", "rb")
            check = pickle.load(infile)
            infile.close()
            initialP = pickle.load(infileP)
            print("Purchase prices:")
            print(initialP)
            infileP.close()
            if initialP == '':
                raise EOFError

            walletAddress = check
            lay = existingLoad(driver, walletAddress, initialP)
            window.close()
            mainScreen(lay)
            break
        except EOFError:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Close":
                break
            elif event == "Continue":
                outfile = open("localInfo.pickle", 'wb')
                pickle.dump(values[0], outfile)
                outfile.close()

                walletAddress = values[0].strip()
                window.close()
                tokenAmountScreen()
                break
    window.close()


# If the user decides to go back to the address screen to input a new address,
# this function will run
def backInputAddress():
    layout = [[sg.Text('Enter your BEP20 Wallet Address')],
    [sg.InputText(size=(42,20))],
    [sg.Sizer(185,0), sg.Button('Continue'), sg.Button("Close", pad=(5,12))]
    ]

    window = sg.Window("BEP20 Token Tracker", layout, margins=(50,50), icon=r"C:\Users\andre\Downloads\favicon.ico")
    while True: 
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Close":
                break
            elif event == "Continue":
                outfile = open("localInfo.pickle", 'wb')
                pickle.dump(values[0], outfile)
                outfile.close()

                walletAddress = values[0].strip()
                window.close()
                tokenAmountScreen()
                break
    window.close()


# If user enters an invalid wallet address, this screen will prompt them to retry
def reInputAddress():
    layout = [[sg.Text('Re-enter your BEP20 Wallet Address', font=fnt)],
    [sg.Text('Invalid wallet address! Please try again.')],
    [sg.InputText(size=(42,20))],
    [sg.Sizer(185,0),sg.Button('Continue'), sg.Button("Close", pad=(5,12))]
    ]

    window = sg.Window("BEP20 Token Tracker", layout, margins=(50,50), icon=r"C:\Users\andre\Downloads\favicon.ico")
    while True: 
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Close":
                break
            elif event == "Continue":
                outfile = open("localInfo.pickle", 'wb')
                pickle.dump(values[0], outfile)
                outfile.close()

                walletAddress = values[0].strip()
                window.close()
                tokenAmountScreen()
                break
    window.close()


# If program has not been run before, ask the user for purchase prices of each
# token. Once user presses 'continue', program will gather token data via the
# existingLoad() function and proceed to mainScreen().
def tokenAmountScreen():
    infile = open("localInfo.pickle", "rb")
    check = pickle.load(infile)
    walletAddress = check

    infileP = open("pPrices.pickle", "rb")
    
    try:
        initialP = pickle.load(infileP)
    except EOFError:
        initialP = []
        print('eoferror')

    layoutPrice = []
    inputPrice = []
    table = tokenNames_PP(driver, walletAddress)
    print(table)
    
    i = 0
    for token in table:
        if initialP == [] or initialP == '':
            layoutPrice.append([sg.Text(token, justification='center')])
            inputPrice.append([sg.Input(size=(14,15))])

        elif initialP != []:
            layoutPrice.append([sg.Text(token, justification='center')])
            inputPrice.append([sg.Input(initialP[i], size=(14,15))])
            i = i + 1
 
    
    layout = [[sg.Text('Enter the purchase price or average price of your tokens', font=fnt, justification='center')],
    [sg.Sizer(12,0), sg.Text("If you don't remember, please input 1 instead and continue", justification='center')],
    [sg.Sizer(65,20), sg.Frame(layout=layoutPrice, title=''), sg.Frame(layout=inputPrice, title= '')],
    [sg.Button('Back', pad=(5,12)), sg.Sizer(220,0), sg.Button('Continue'), sg.Button("Close", pad=(5,12))]
    ]
    
    window = sg.Window("BEP20 Token Tracker", layout, margins=(50,50), icon=r"C:\Users\andre\Downloads\favicon.ico")
    while True: 
        if table == []:
            window.close()
            reInputAddress()
            break
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Close":
            break
        elif event == "Continue":
            outfile = open("pPrices.pickle", 'wb')
            listOfPPrices = []
            i = 0
            while i < len(values):
                values[i] = float(values[i])
                print(values[i])
                listOfPPrices.append(values[i])
                i = i + 1
            pickle.dump(listOfPPrices, outfile)
            outfile.close()

            lay = existingLoad(driver, walletAddress, listOfPPrices)
            window.close()
            mainScreen(lay)
            break
        elif event == 'Back':
            window.close()
            outfile = open("pPrices.pickle", 'wb')
            pickle.dump('', outfile)
            outfile.close()
            backInputAddress()
            break
    window.close()


# Displays BEP20 wallet address holding and related info.
# Takes layout argument which is created in the existingLoad() function
def mainScreen(layout):
    window = sg.Window("BEP20 Token Tracker", layout, margins=(50,50), icon=r"C:\Users\andre\Downloads\favicon.ico")
    while True: 
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Close":
            break
        elif event == 'Back':
            window.close()
            tokenAmountScreen()
            break
        
    window.close()




