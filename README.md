# BEP20TokenTracker
This program uses Selenium and PySimpleGUI to attain token holdings and related 
info for any BEP20 address. 

When this program is first run, you are prompted to input your BEP20 wallet 
address and the initial purchase prices (or average price) for all of your token
holdings. Then, a window will be generated which displays each of your BEP20
token holdings and related info (current price, holding amount, PL %, value).

Once you run the program once and input your wallet address and initial purchase
prices, these values will be stored in a pickle file which the program will
use on successive runs so you do not need to add this information again. 

