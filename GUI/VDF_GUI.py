import time
import os
import yaml
import openpyxl
import pandas as pd
import logger
import tool
import issus

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

config = yaml.load(open(os.path.abspath(os.path.join(os.getcwd(), os.path.pardir)+'\DG4278_config.yml')), Loader=yaml.Loader)
file = 'DG4278'
component_title = []
time_string = datetime.now().strftime('%Y-%m-%d')

dev_logger = logger.get_logger(__name__)

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')                 # 瀏覽器不提供可視化頁面
    options.add_argument('-no-sandbox')               # 以最高權限運行
    options.add_argument('--start-maximized')        # 縮放縮放（全屏窗口）設置元素比較準確
    options.add_argument('--disable-gpu')            # 谷歌文檔說明需要加上這個屬性來規避bug
    options.add_argument('--window-size=1920,1080')  # 設置瀏覽器按鈕（窗口大小）
    options.add_argument('--incognito')               # 啟動無痕

    driver = webdriver.Chrome(options=options)
    url = config['DG4278_url']

    # driver.implicitly_wait(10)
    # driver.get(url)
    # driver.delete_all_cookies() #清cookie
    
    # with open("cookies.yml", "r") as f:
    #     cookies = yaml.safe_load(f)
    #     for c in cookies:
    #         if 'domain' in c:
    #             c['domain'] = 'xxx'
    #         dev_logger.info(c)
    #         driver.add_cookie(c)

    driver.get(url)
    

    return driver

def main(first_component, second_component):
    try:
        start = time.time()
        driver = get_driver()
        
        login(driver)
        dev_logger.info('Wait for check project...')
        check_project(driver)
        dev_logger.info('Go to get components name')
        get_components_name(driver)        
        dev_logger.info('Go to get issus')
        get_issus(driver, first_component, second_component)
        
        end = time.time()
        dev_logger.info('Time elapsed: ' + str(start-end) + ' seconds')

    except Exception as e:
        dev_logger.critical(e, exc_info=True)
        # input('Exit')
        
def login(driver):
    dev_logger.info('Waiting for login...')
    tool.Wait_Id(driver, 'i0116').send_keys(config['DG4278_username']) 
    tool.Wait_Id(driver, 'idSIButton9').click() 
    time.sleep(3)
    tool.Wait_Id(driver, 'i0118').send_keys(config['DG4278_password']) 
    tool.Wait_Id(driver, 'idSIButton9').click() 
    number = tool.Wait_Id(driver, 'idRichContext_DisplaySign').text
    dev_logger.info(f'Please enter number on your phone: {number}')
    time.sleep(8)
    tool.Wait_Id(driver, 'idSIButton9').click() 
    dev_logger.info('Waiting for the website to load...')
    # cookie2 = driver.get_cookies() #取得登入後cookie
    # with open("cookies.yml", "w") as f:
    #     yaml.safe_dump(data=cookie2, stream=f)

def check_project(driver):
    header_li = tool.Wait_Xpath(driver, '//*[@id="header"]/nav/div/div[2]/ul').find_elements(By.TAG_NAME, 'li')
    p=0
    for h, hd in enumerate(header_li):
        time.sleep(1)
        if p == 1:
            break
        # print(hd.text)
        if hd.text == 'Projects':
            tool.Wait_Id(driver, 'browse_link').click()
            if tool.Wait_Id(driver, 'admin_main_proj_link_lnk').text == 'CPE Global Requirements (CPEGR)':
                break
            else:
                history_li = tool.Wait_Xpath(driver, '//*[@id="project_history_main"]/ul').find_elements(By.TAG_NAME, 'li')
                for h, ht in enumerate(history_li):
                    time.sleep(1)
                    # print(ht.text)
                    if ht.text == 'CPE Global Requirements (CPEGR)':
                        tool.Wait_Id(driver, ht.get_attribute('id')).click()
                        p+=1
                        break
        else:
            continue
                        
def get_components_name(driver):
    sidebar_li = tool.Wait_Xpath(driver, '//*[@id="sidebar"]/div/div[1]/nav/div/div/ul').find_elements(By.TAG_NAME, 'li')
    for s, sb in enumerate(sidebar_li):
        if sb.text == 'Components':                                                                                         
            components_page = tool.Wait_Xpath(driver, '//*[@id="sidebar"]/div/div[1]/nav/div/div/ul/li[' + str(s+1) +']/a')
            actions = ActionChains(driver)
            actions.click(components_page).perform()
            break    
    tool.Wait_Xpath(driver, '//*[@id="sidebar-page-container"]/div[1]/div/div/h1')
    components = tool.Wait_Xpath(driver, '//*[@id="components-table"]/tbody[2]').find_elements(By.TAG_NAME, 'tr')
    for title in components:
        new_titile = title.find_elements(By.TAG_NAME, 'td')[0].text.strip().replace("/", "")
        component_title.append(new_titile)
    
    component_data = component(driver)
    components_df = pd.DataFrame(component_data)
    
    with pd.ExcelWriter(f'{time_string}{file}.xlsx', mode="w+", engine="openpyxl") as writer:
        components_df.to_excel(writer, sheet_name='components', index=False)

def component(driver):
    component_data = {}
    Component_text = tool.Wait_Xpath(driver, '//*[@id="sidebar-page-container"]/div[1]/div/div/h1').text
    dev_logger.info(f'Turn to page {Component_text}.')
    if Component_text == 'Components':
        components_table = tool.Wait_Xpath(driver, '//*[@id="components-table"]/tbody[1]/tr').find_elements(By.TAG_NAME, 'th')
        for components_th in components_table:
            component_data[components_th.text]=[]
        
        item_state_ready = tool.Wait_Xpath(driver, '//*[@id="components-table"]/tbody[2]').find_elements(By.TAG_NAME, 'tr')
        for issus_tr in item_state_ready:
            component_data[list(component_data.keys())[0]].append(issus_tr.find_elements(By.TAG_NAME, 'td')[0].text.strip())
            component_data[list(component_data.keys())[1]].append(issus_tr.find_elements(By.TAG_NAME, 'td')[1].text.strip())
            component_data[list(component_data.keys())[2]].append(issus_tr.find_elements(By.TAG_NAME, 'td')[2].text.strip())
            component_data[list(component_data.keys())[3]].append(issus_tr.find_elements(By.TAG_NAME, 'td')[3].text.strip())
            component_data[list(component_data.keys())[4]].append(issus_tr.find_elements(By.TAG_NAME, 'td')[4].text.strip())
            component_data[list(component_data.keys())[5]].append(issus_tr.find_elements(By.TAG_NAME, 'td')[5].text.strip())
            component_data[list(component_data.keys())[6]].append(issus_tr.find_elements(By.TAG_NAME, 'td')[6].text.strip())
    
    return component_data

        
def get_issus(driver, first_component, second_component):
    if first_component in component_title and second_component in component_title:
        for i in range(component_title.index(first_component), component_title.index(second_component)+1):
            check_page = tool.Xpath(driver, '//*[@id="components-table"]/tbody[2]/tr[' + str(i+1) +']/td[1]/div/a')
            
            # print(check_page.text.replace("/", ""), component_title[i])
            if check_page.text.replace("/", "") == component_title[i]:
                    check_page.click()
            issus_data = issus.issus(driver, config)
            dev_logger.info('Go to excel.')
            issus_df = pd.DataFrame(issus_data)
            with pd.ExcelWriter(f'{time_string}{file}.xlsx', mode="a", engine="openpyxl") as writer:
                df = issus_df.fillna('').astype(str)
                for col in df.columns:
                    df[col] = df[col].apply(lambda x: tool.data_clean(x))
                df.to_excel(writer, sheet_name=component_title[i], index=False)
            dev_logger.info(f'{component_title[i]} data appended successfully.')
            jira= tool.Wait_Xpath(driver, '//*[@id="logo"]/a')
            if jira.text == 'CPS Jira':
                jira_text = jira.text
                jira.click()
                dev_logger.info(f'Turn to page {jira_text}.')

if __name__ == '__main__':
    # first_component = input('First component: ')
    # second_component = input('Second component(If only need to inquire one, enter the same as the first component): ')
    first_component = 'Wireless Module'
    second_component = 'Wireless Module'
    main(first_component, second_component)