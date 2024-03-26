import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

timeout = 20

def Xpath(driver, x):
    return driver.find_element(By.XPATH, x)

def Wait_Xpath(driver, wx):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, wx)))
                                                                                
def Wait_Id(driver, wd):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, wd)))

def ClassName(driver, c):
    return driver.find_element(By.CLASS_NAME, c)

def data_clean(text):
    # 清洗excel中的非法字符，都是不常見的不可顯示字符，例如退格，響鈴等
    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
    text = ILLEGAL_CHARACTERS_RE.sub(r'', text)
    return text

def next_iselement(driver):
    try:
        ClassName(driver, 'nav-next')
        return True
    except:
        return False

def load_more(driver):
    try:
        ClassName(driver, 'css-9duhdc')
        return True
    except:
        return False
    
def check_description(driver):
    try:
        Xpath(driver, '//*[@id="descriptionmodule-label"]')
        return True
    except:
        return False
    
def check_opco(driver):
    try:
        Xpath(driver, '//*[@id="rowForcustomfield_24326"]/div/strong/label')
        return True
    except:
        return False
