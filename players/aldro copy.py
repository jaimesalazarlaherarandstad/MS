from pyautogui import PAUSE, moveTo, click, mouseDown, mouseUp

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from time import sleep

from conf import *




def scrape(driver, fullAddress, monthlyBill):

    print('Processing Aldro with address ' + fullAddress + ' and bill ' + monthlyBill)

    PAUSE = 0.4
    roofDrawClickPause = 1

    driver.get(URL_ALDRO)

    searchBox = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pac-input1"]')))
    searchBox.send_keys(fullAddress)
    sleep(1)
    searchBox.send_keys(Keys.DOWN)
    searchBox.send_keys(Keys.TAB)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="cargaLocalizacion"]'))).click()

    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="cargaMapaEditable"]'))).click()
    
    for i in range(0,5):
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="map"]/div/div/div[8]/div/div/button[1]'))).click()
    
    sleep(2)

    selectedCoords = {}
    if 'Asturias' in fullAddress:
        selectedCoords = COORDS_ALDRO['Asturias']
    elif 'Ávila' in fullAddress:
        selectedCoords = COORDS_ALDRO['Ávila']

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

    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="paso4"]'))).click()
    # nextButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="paso4"]')))
    # driver.execute_script("arguments[0].click();", nextButton)

    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="tejado30"]'))).click()
    
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datosFactura"]'))).click()
    sleep(2)
    click(x=610, y=530)

    billElement = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="gastoManual"]')))
    billElement.click()
    billElement.send_keys(monthlyBill)

    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[6]/div[1]/div/div[2]/div/div/div/div/div[1]/div').click()
    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div').click()

    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[6]/div[1]/div/div[3]/div/div/div/div[2]/div').click()
    
    driver.find_element_by_xpath('//*[@id="calcularSolicitud"]').click()

    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/div[1]/div/div/div[7]/div/div[2]/div/div[3]/p/span')))
      
    # requestButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="simulator-toolbar"]/div[2]/button')))
    # while not requestButton.is_enabled():
    #     print('Waiting for values to load')
    # sleep(2)

    out = {}

    out[POWER_PANEL]  = driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[7]/div/div[2]/div/div[1]/div/div[1]/div[3]/p/strong[2]').text.replace('Wp.','')
    out[COST_TOTAL] = driver.find_element_by_xpath('//*[@id="precioPack"]').text.replace('€','').split(',')[0].replace('.','') # could round instead
    out[NUM_PANELS] = driver.find_element_by_xpath('//*[@id="numeroPaneles"]/span').text
    out[POWER_TOTAL] = driver.find_element_by_xpath('//*[@id="kilovatioPico"]/span').text.replace(',','.')

    for key in out:
        out[key] = out[key].strip()

    return out