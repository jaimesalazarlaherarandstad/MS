from pyautogui import PAUSE, moveTo, click, mouseDown, mouseUp

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from time import sleep

from conf import *


from selenium.webdriver.common.action_chains import ActionChains



def scrape(driver, fullAddress, monthlyBill):

    print('Processing Gesternova with address ' + fullAddress + ' and bill ' + monthlyBill)

    PAUSE = 0.4
    roofDrawClickPause = 1

    driver.get(URL_GESTERNOVA)

    searchBox = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="addressLocatorField"]')))
    searchBox.send_keys(fullAddress)
    searchBox.send_keys(Keys.ENTER)

    for i in range(0,5):
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="map"]/div/div/div[9]/div/div/button[1]'))).click()



    # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

    selectedCoords = {}
    if 'Asturias' in fullAddress:
        selectedCoords = COORDS_GESTERNOVA['Asturias']
    elif 'Ávila' in fullAddress:
        selectedCoords = COORDS_GESTERNOVA['Ávila']

    # # Roof clicks work better with a move, a pause, and THEN a click
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

    continueButton = driver.find_element_by_xpath('//*[@id="nextStep3"]')
    driver.execute_script("arguments[0].scrollIntoView();", continueButton)
    continueButton.click()

    continueButton = driver.find_element_by_xpath('//*[@id="nextStep4"]')
    driver.execute_script("arguments[0].scrollIntoView();", continueButton)
    continueButton.click()


    sliderElement = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="budget"]')))
    # print(sliderElement.location['x'])
    # print(sliderElement.location['y'])

    billElement = driver.find_element_by_xpath('//*[@id="rangePrice"]')
    billOnScreen = billElement.get_attribute("value").replace(' €', '')
    # driver.execute_script("arguments[0].scrollIntoView();", billElement)

    # input('Waiting')


    lastX = 420 # lastX = sliderElement.location['x'] seems to be 417 (vs 480 or 480 with scroll)
    y = 680     # y = sliderElement.location['y'] seems to be 528 (vs 400 or 215 with scroll)
    while billOnScreen != monthlyBill:

        moveTo(x=lastX, y=y)      
        mouseDown()

        lastX = lastX + 15
        moveTo(x=lastX, y=y)      
        mouseUp()

        billOnScreen = driver.find_element_by_xpath('//*[@id="rangePrice"]').get_attribute("value").replace(' €', '')
        print('billOnScreen = ' + billOnScreen)


    continueButton = driver.find_element_by_xpath('//*[@id="sendRequestBtn"]')
    driver.execute_script("arguments[0].scrollIntoView();", continueButton)
    continueButton.click()
    
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="submitButton"]')))

    out = {}

    out[NUM_PANELS] = driver.find_element_by_xpath('//*[@id="invoice"]/div[1]/div[1]/div/div[1]/p[2]/span').text
    out[POWER_TOTAL] = driver.find_element_by_xpath('//*[@id="invoice"]/div[1]/div[1]/div/div[2]/p[2]/span[1]').text
    out[POWER_PANEL]  = str(int(float(out[POWER_TOTAL])/int(out[NUM_PANELS]) * 1000))
    out[COST_TOTAL] = driver.find_element_by_xpath('//*[@id="invoice"]/div[1]/div[2]/p[2]/span[1]').text.split(',')[0].replace('.','') # could round instead
    
    financedDownPayment = driver.find_element_by_xpath('//*[@id="invoice"]/div[1]/div[2]/div[2]/p[2]/span').text
    financedMonthlyQuote = driver.find_element_by_xpath('//*[@id="invoice"]/div[1]/div[2]/div[2]/p[3]/span').text
    out[COST_MONTHLY_FINANCED] = str(float(financedDownPayment)/12 + float(financedMonthlyQuote))
    
    savings25years = int(driver.find_element_by_xpath('//*[@id="invoice"]/div[2]/div/div[1]/div[1]/div[2]/span[2]').text.split(',')[0].replace('.',''))
    out[SAVINGS_YEARLY] = str(savings25years/25)

    out[SELF_CONSUMPTION_PERCENTAGE] = driver.find_element_by_xpath('//*[@id="invoice"]/div[2]/div/div[2]/div/div/span').text

    for key in out:
        out[key] = out[key].strip()

    return out