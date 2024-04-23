import time
import logger
import tool

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

dev_logger = logger.get_logger(__name__)

timeout = 20

def issus(driver, config):
    issus_data = {}
    issus_text = tool.Wait_Xpath(driver, '//*[@id="search-header-view"]/div/h1').text
    dev_logger.info(f'Turn to page {issus_text}.')

    #get value from issus title
    try:
        if issus_text == 'Search':
            time.sleep(1)
            issus_th = driver.find_element(By.XPATH, '//*[@id="issuetable"]/thead/tr').find_elements(By.TAG_NAME, 'th')
            for i in range(1, len(issus_th)):
                issus_th = driver.find_element(By.XPATH, '//*[@id="issuetable"]/thead/tr/th[' + str(i) +']/span').text
                if issus_th != 'Reporter':
                    issus_data[issus_th]=[]
                    
    except Exception as e:
        dev_logger.critical(e, exc_info=True)


    #get value from issus page information
    total = 0
    issus_data['OpCo']=[]
    issus_data['Description']=[]
    # issus_data['Link']=[]
    # issus_data['Name']=[]
    # issus_data['status-lozenge']=[]
    # issus_data['last-execution-status']=[]
    # issus_data['play-button']=[]
    # issus_data['remove-button']=[]
    while True:
        tbody = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody'))).find_elements(By.TAG_NAME, 'tr')
        for issus_tr in tbody:
            dev_logger.info(f"Now at {issus_tr.find_elements(By.TAG_NAME, 'td')[1].text.strip()}.")
            WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="search-header-view"]/div/h1')))
            issus_data[list(issus_data.keys())[0]].append(issus_tr.find_elements(By.TAG_NAME, 'td')[0].text.strip())
            issus_data[list(issus_data.keys())[1]].append(issus_tr.find_elements(By.TAG_NAME, 'td')[1].text.strip())
            issus_data[list(issus_data.keys())[2]].append(issus_tr.find_elements(By.TAG_NAME, 'td')[2].text.strip())
            issus_data[list(issus_data.keys())[3]].append(issus_tr.find_elements(By.TAG_NAME, 'td')[3].text.strip())
            issus_data[list(issus_data.keys())[4]].append(issus_tr.find_elements(By.TAG_NAME, 'td')[4].text.strip())
            issus_data[list(issus_data.keys())[5]].append(issus_tr.find_elements(By.TAG_NAME, 'td')[5].text.strip())
            
            #Go to description
            try:
                time.sleep(2)    
                # print(issus_tr.find_elements(By.TAG_NAME, 'td')[1].find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
                
                #開啟新分頁
                href = issus_tr.find_elements(By.TAG_NAME, 'td')[1].find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                # print(href)
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1]) 
                driver.get(href)
                
                time.sleep(2)
                
                WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="project-name-val"]')))
                #OpCo
                if tool.check_opco(driver) == True:
                    opco_text = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="customfield_24326-field"]/span'))).text.strip()
                    issus_data[list(issus_data.keys())[6]].append(opco_text)
                else:
                    issus_data[list(issus_data.keys())[6]].append('')

                #Description
                key_text = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="key-val"]'))).text.strip()
                summary_text = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="summary-val"]'))).text.strip()

                if tool.check_description(driver) == True:
                    description_text = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="descriptionmodule"]/div[2]'))).text.strip()
                    # print(description_text)
                    if key_text == list(issus_data.values())[1][-1] and summary_text == list(issus_data.values())[2][-1]:
                        issus_data[list(issus_data.keys())[7]].append(description_text)
                else:
                    issus_data[list(issus_data.keys())[7]].append('')
            
            except Exception as e:
                dev_logger.critical(e, exc_info=True)
                    
            # #Traceability
            # try:                                                                                                          
            #     no_textcase = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ZephyrScaleIssuePanel"]/span/section/main/div/span[2]'))).text 
            #     if 'No test cases.' in no_textcase:
            #         # pass
            #         issus_data[list(issus_data.keys())[8]].append('')
            #         issus_data[list(issus_data.keys())[9]].append('')
            #         issus_data[list(issus_data.keys())[10]].append('')
            #         issus_data[list(issus_data.keys())[11]].append('')
            #         # issus_data[list(issus_data.keys())[12]].append('')
            # except:
            #     total_div = []
            #     if tool.load_more(driver) == True:
            #         total_li = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-9duhdc'))).find_elements(By.TAG_NAME, 'div')
            #         for i in total_li:
            #             total_div.append(i.text)

            #         load_check = (int((total_div[-1][-2:].strip()))-1)/5   #暫時用-1的方式，以達除完有餘數
            #         WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ZephyrScaleIssuePanel"]/span/section/main/h2')))
            #         for click in range(int(load_check)):
            #             WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-rvtbkj'))).click()
            #             time.sleep(3)

            #     textcase = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, 'css-afeyfj'))).find_elements(By.TAG_NAME, 'li')
            #     # print(len(textcase))
            #     a = 0 #第一行省略
            #     for issus_span in textcase:
            #         # WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'span')))
            #         # dev_logger.info(issus_span.find_elements(By.TAG_NAME, 'span')[6].get_attribute('aria-label'))
            #         if a != 0:
            #             issus_data[list(issus_data.keys())[0]].append('')
            #             issus_data[list(issus_data.keys())[1]].append('')
            #             issus_data[list(issus_data.keys())[2]].append('')
            #             issus_data[list(issus_data.keys())[3]].append('')
            #             issus_data[list(issus_data.keys())[4]].append('')
            #             issus_data[list(issus_data.keys())[5]].append('')
            #             issus_data[list(issus_data.keys())[6]].append('')
            #             issus_data[list(issus_data.keys())[7]].append('')

            #         issus_data[list(issus_data.keys())[8]].append(issus_span.find_element(By.CLASS_NAME, 'css-17wby6x').text.strip())
            #         issus_data[list(issus_data.keys())[9]].append(issus_span.find_element(By.CLASS_NAME, 'css-tyqob8').text.strip())
            #         issus_data[list(issus_data.keys())[10]].append(issus_span.find_element(By.CLASS_NAME, 'css-1mbo33i').text.strip())
            #         issus_data[list(issus_data.keys())[11]].append(issus_span.find_elements(By.TAG_NAME, 'div')[3].get_attribute('aria-label'))
            #         # issus_data[list(issus_data.keys())[12]].append(issus_span.find_elements(By.TAG_NAME, 'span')[6].get_attribute('aria-label'))
            #         # issus_data[list(issus_data.keys())[13]].append(issus_span.find_elements(By.TAG_NAME, 'span')[8].get_attribute('aria-label'))

            #         a += 1
           
            dev_logger.info(f'Description and Test Cases has been added to {key_text}.')
            #關掉新分頁，回到原本的頁面
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(2)

        # for key, value in issus_data.items():
        #     print(key, len([item for item in value if item]))

        total+=(len(tbody))
        results = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div/div/div[2]/div[1]/span'))).text
        if tool.next_iselement(driver) == True:
            next = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'nav-next')))
            actions = ActionChains(driver)
            actions.click(next).perform()

            check_title = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div/div/div[2]/div[2]/div/strong'))).text
            dev_logger.info(f'{results} , Currently on page {check_title}.')

        else:
            dev_logger.info(results)

        # print(total)
        time.sleep(2)
        check_results = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div/div/div[2]/div[1]/span/span[3]'))).text
        # print(issus_data.keys())
        # if (total == 25): 
        if (total == int(check_results)): 
            break
    
    return issus_data
