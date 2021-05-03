# defiTokenTracker
This program uses Selenium and PySimpleGUI to attain token holdings and related 
info for any BEP20 address. 

If you want to use this program for your own wallet, you must update the 
walletAddress variable with your BEP20 wallet address and manually input the 
purchase price for each token. If you do not care for the profit/loss percent
for some tokens, input the purchase price as 0.

If you would like to test changes in the program, I suggest setting the sleep
time on line 52 of getTokens.py to 1. This will allow for the program to load
faster and for you to check the outcome of your changes. However, this will
also result in the token data being inaccurate.

