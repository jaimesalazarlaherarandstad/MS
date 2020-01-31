from pyautogui import PAUSE, moveTo, mouseDown, mouseUp

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By

from time import sleep

from conf import *

from helpers import printDict
from pyautogui import alert


def scrape(driver, province, monthlyBill):

    print('Processing Powen with address ' + province + ' and bill ' + monthlyBill)

    PAUSE = 1
    
    driver.get(URL_POWEN)
    driver.refresh()      # seems to be required for Powen, otherwise it won't reload the calculator
    sleep(3)

    calculateButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="first_set"]/input')))
    driver.execute_script("arguments[0].click();", calculateButton)  

    houseButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vivienda"]')))
    driver.execute_script("arguments[0].click();", houseButton)
    sleep(2)

    nextButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="type_fileset"]/input')))
    driver.execute_script("arguments[0].click();", nextButton)
    sleep(5)

    sliderElement = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,'gasto_mensual')))
    
    print('sliderElement.location[x] = ', sliderElement.location['x'])
    print('sliderElement.location[y] = ', sliderElement.location['y'])

    # sleep(2)
   
    billOnScreen = driver.find_element_by_xpath('//*[@id="amount"]').text
    # input('Waiting')
    lastX = 480 # lastX = sliderElement.location['x'] seems to be 452 (vs 480)
    y = 400     # y = sliderElement.location['y'] seems to be 1098 (vs 400)
    count = 0
    while billOnScreen != monthlyBill:

        moveTo(x=lastX, y=y)      
        mouseDown()

        lastX = lastX + 15
        moveTo(x=lastX, y=y)      
        mouseUp()

        billOnScreen = driver.find_element_by_xpath('//*[@id="amount"]').text
        print('billOnScreen = ' + billOnScreen)

        # Seems like the refresh shifts elements up or down
        # If can't find slider element, try the other possible position
        if count == 30:
            lastX = 480     # x doesn't change but must be restarted
            y = 350         # seems like if y is not 400, it must be 350
        
        count += 1


    driver.find_element_by_xpath('//*[@id="dia"]/li').click()
    driver.find_element_by_xpath('//*[@id="tarde"]/li').click()
    
    select = Select(driver.find_element_by_xpath('//*[@id="provincias"]'))
    # print(select)

    options = select.options

    selectValue = 0
    for option in options:
        value = option.get_attribute("value")
        text = option.get_attribute("text")
        # print(value + ': ' + text)
        if text == province:
            selectValue = value

    select.select_by_value(selectValue)

    calculateButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="second_fieldset"]/input[2]')))
    driver.execute_script("arguments[0].click();", calculateButton)

    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="multiform"]/label[15]/input')))

    out = {}

    out[POWER_TOTAL] = driver.find_element_by_xpath('//*[@id="potencia_instalar"]').text.replace(' kWp','')
    out[NUM_PANELS] = driver.find_element_by_xpath('//*[@id="n_paneles"]').text
    out[COST_TOTAL] = driver.find_element_by_xpath('//*[@id="precio_venta"]').text.replace('€','').replace('.','').split(',')[0]
    out[SAVINGS_SELF_CONSUMPTION] = driver.find_element_by_xpath('//*[@id="ahorro_mensual"]').text.replace('€','').split(',')[0]
    
    for key in out:
        out[key] = out[key].strip()
    
    return out