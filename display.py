from displayTokens import inputAddress
import pickle
import PySimpleGUI as sg

fnt = "Arial 11"

layout = [[sg.Text('Would you like to restore your last session?', font=fnt, justification='center')],
    [sg.Sizer(92,0), sg.Button("Yes", pad=(5,10)), sg.Button(" No ", pad=(25,10))],
    [sg.Sizer(240,0), sg.Button("Close", pad=(5,12))]]

window = sg.Window("BEP20 Token Tracker", layout, margins=(30,30), icon=r"C:\Users\andre\Downloads\favicon.ico")
while True:
    event, values = window.read()
    if event == 'Yes':
        window.close()
        inputAddress()
        break
    elif event == ' No ':
        outfile = open("pPrices.pickle", 'wb')
        pickle.dump('', outfile)
        outfile.close()
        window.close()
        inputAddress()
        break
    elif event == 'Close' or event == sg.WIN_CLOSED:
        break
window.close()
