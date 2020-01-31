from conf import *

import sys

from selenium.webdriver import Chrome
from pyautogui import click, alert

from players import repsol, naturgy, powen, aldro, gesternova

from helpers import printDict


numLocations = int(sys.argv[1])
numBills = int(sys.argv[2])

print('Processing ', numLocations, ' locations and ', numBills, ' bills')

with Chrome() as driver:

    click(x=877, y=26)
    
    for player in PLAYERS:

        if player == 'Repsol':
            selectedScrape = repsol.scrape
            selectedLocations = ADDRESSES
            selectedBills = MONTHLY_BILLS
        elif player == 'Naturgy':
            selectedScrape = naturgy.scrape
            selectedLocations = PROVINCES
            selectedBills = YEARLY_CONSUMPTIONS
        elif player == 'Powen':
            selectedScrape = powen.scrape
            selectedLocations = PROVINCES
            selectedBills = MONTHLY_BILLS
        elif player == 'Aldro':
            selectedScrape = aldro.scrape
            selectedLocations = ADDRESSES
            selectedBills = MONTHLY_BILLS
        elif player == 'Gesternova':
            selectedScrape = gesternova.scrape
            selectedLocations = ADDRESSES
            selectedBills = MONTHLY_BILL_RANGES
        else:
            alert('Player ' + player + ' not recognized')
            sys.exit(1)

        for idxLocation, location in enumerate(selectedLocations):
            if idxLocation == numLocations: break

            for idxBill, bill in enumerate(selectedBills):
                if idxBill == numBills: break

                out = selectedScrape(driver, location, bill)
                printDict(out)

                input('Waiting')

            # TODO: save to Excel
