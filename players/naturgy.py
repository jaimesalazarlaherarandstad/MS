from pyautogui import PAUSE

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By

from time import sleep

from conf import *




def scrape(driver, province, yearlyConsumption):

    print('Processing Naturgy with address ' + province + ' and bill ' + yearlyConsumption)

    PAUSE = 0.4

    driver.get(URL_NATURGY)

    name = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="name"]')))
    name.send_keys(' ' + '\t')
    
    select = Select(driver.find_element_by_xpath('//*[@id="provincia"]'))
    options = select.options

    selectValue = 0
    for option in options:
        value = option.get_attribute("value")
        text = option.get_attribute("text")
        # print(value + ': ' + text)
        if text == province:
            selectValue = value

    select.select_by_value(selectValue)
    
    billElement = driver.find_element_by_xpath('//*[@id="consumo"]')
    billElement.click()
    billElement.send_keys(Keys.CONTROL + 'a')
    billElement.send_keys(Keys.DELETE)
    billElement.send_keys(yearlyConsumption)
    
    calculateButton = driver.find_element_by_xpath('/html/body/div/div/form/div[2]/div[2]/input').click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/h2')))
    sleep(2)

    out = {}

    out[DESCRIPTION_PANEL] = driver.find_element_by_xpath('/html/body/div/div/div[1]/ul/li[1]').text.replace('Paneles fotovoltaicos: ','')
    # print('out[DESCRIPTION_PANEL] = ' +  out[DESCRIPTION_PANEL])

    index = out[DESCRIPTION_PANEL].find(' Wp')
    # print('index = ' + str(index))

    out[POWER_PANEL] = out[DESCRIPTION_PANEL][index-3:index]
    # print('out[POWER_PANEL] = ' + out[POWER_PANEL])

    out[NUM_PANELS] = out[DESCRIPTION_PANEL].replace(' módulos Vision 60M '+out[POWER_PANEL]+' Wp','')
        
    out[POWER_TOTAL] = str((int(out[NUM_PANELS]) * int(out[POWER_PANEL])) / 1000)
    out[DESCRIPTION_INVERTER] = driver.find_element_by_xpath('/html/body/div/div/div[1]/ul/li[2]').text.replace('Inversor: ','')
    out[SAVINGS_PERCENT] = driver.find_element_by_xpath('/html/body/div/div/div[1]/div[1]/div[1]/span').text.replace('%','')
    out[COST_TOTAL] = str(float(driver.find_element_by_xpath('/html/body/div/div/div[1]/div[1]/div[2]/span').text.replace(' €','').replace('.','').replace(',','.')) * 1.21)
    out[SAVINGS_SELL_BACK] = driver.find_element_by_xpath('/html/body/div/div/div[1]/div[2]/div[2]/p/span').text.replace('-','').replace('€/año','')

    for key in out:
        out[key] = out[key].strip()

    return out