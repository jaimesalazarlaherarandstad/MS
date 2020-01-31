from pyautogui import PAUSE, moveTo, click, mouseDown, mouseUp

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from time import sleep

from conf import *




def scrape(driver, fullAddress, monthlyBill):

    print('Processing Repsol with address ' + fullAddress + ' and bill ' + monthlyBill)

    PAUSE = 0.4
    roofDrawClickPause = 1

    driver.get(URL_REPSOL)

    searchBox = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,'searchBox')))
    searchBox.send_keys(fullAddress)
    sleep(1)
    searchBox.send_keys(Keys.ENTER)
    
    continueButton = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,'startDrawing')))
    continueButton.click()

    selectedCoords = {}
    if 'Asturias' in fullAddress:
        selectedCoords = COORDS_REPSOL['Asturias']
    elif 'Ávila' in fullAddress:
        selectedCoords = COORDS_REPSOL['Ávila']

    # Roof clicks work better with a move, a pause, and THEN a click
    moveTo(x=selectedCoords['1'][0], y=selectedCoords['1'][1]) 
    sleep(roofDrawClickPause)
    click()

    moveTo(x=selectedCoords['2'][0], y=selectedCoords['2'][1]) 
    sleep(roofDrawClickPause)
    click()

    moveTo(x=selectedCoords['3'][0], y=selectedCoords['3'][1]) 
    sleep(roofDrawClickPause)
    click()

    moveTo(x=selectedCoords['4'][0], y=selectedCoords['4'][1]) 
    sleep(roofDrawClickPause)
    click()

    moveTo(x=selectedCoords['1'][0], y=selectedCoords['1'][1]) 
    sleep(roofDrawClickPause)
    click()

    continueButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="simulator-map-info"]/div[4]/button[3]')))
    continueButton.click()

    sliderButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="sliderPrice"]/span[3]')))

    moveTo(x=780, y=620)
    mouseDown()
    moveTo(x=1110, y=620)
    mouseUp()

    billElement = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="simulator-input-data"]/div/div[1]/div[2]/div[1]/input')))
    billElement.click()
    billElement.send_keys(Keys.CONTROL + 'a')
    billElement.send_keys(Keys.DELETE)
    billElement.send_keys(monthlyBill)
    billElement.send_keys(Keys.HOME)
    billElement.send_keys(Keys.DELETE)

    driver.find_element_by_xpath('//*[@id="simulator-input-data"]/div/div[2]/div/button').click()
    
    requestButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="simulator-toolbar"]/div[2]/button')))
    while not requestButton.is_enabled():
        print('Waiting for values to load')
    sleep(2)

    out = {}

    out[PRODUCTION_ESTIMATE] = driver.find_element_by_xpath('//*[@id="simulator-map-info"]/div[2]/div[2]/p[1]/span[1]').text.replace('.','')
    out[NUM_PANELS] = driver.find_element_by_xpath('//*[@id="number_module"]/div[2]/div[2]').text
    out[POWER_TOTAL] = driver.find_element_by_xpath('//*[@id="installation_power"]/div[2]/div[2]').text.replace(',','.')

    out[POWER_PANEL] = str(float(out[POWER_TOTAL]) / int(out[NUM_PANELS]))

    out[SAVINGS_PERCENT] = driver.find_element_by_xpath('//*[@id="used_roof_area_percentaje"]/div[2]/div[2]').text
    out[COST_TOTAL] = driver.find_element_by_xpath('//*[@id="total_price"]/span[2]').text.replace('.','')
    out[COST_MONTHLY_FINANCED] = driver.find_element_by_xpath('//*[@id="month_price"]/span[3]').text.replace(',','.')
    out[SAVINGS_SELF_CONSUMPTION] = driver.find_element_by_xpath('//*[@id="selfconsumptionSavings"]/span').text.replace('€','')
    out[SAVINGS_SELL_BACK] = str(int(driver.find_element_by_xpath('//*[@id="number_module"]/div[2]/div[2]').text.replace('€','')) + int(driver.find_element_by_xpath('//*[@id="wayletSavings"]/span').text.replace('€','')))
    out[SELF_CONSUMPTION_PERCENTAGE] = driver.find_element_by_xpath('//*[@id="speeder"]/div[1]/span').text.replace('%','')
    out[DESCRIPTION_PANEL] = driver.find_element_by_xpath('//*[@id="benq"]/div').text
    out[DESCRIPTION_INVERTER] = driver.find_element_by_xpath('//*[@id="fronius"]/div').text

    for key in out:
        out[key] = out[key].strip()

    return out