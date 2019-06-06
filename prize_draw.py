from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import time
import re
import random
import sys
import xlrd
import xlwt
from xlutils.copy import copy

def get_h2_text(browser):

    while True:
        ps = browser.page_source
        #time.sleep(1)
        # ps = r'div class="Q__process" data-v-fb80c486=""><div class="Q__bar" data-v-fb80c486="" style="width: 0%;"></div><div id="123" class="Q__text" data-v-fb80c486="">已答题<span data-v-fb80c486="">0</span>/22</div></div>'
        bsObj = BeautifulSoup(ps, 'lxml')
        # print(bsObj)
        elm = bsObj.find('h2', text=re.compile('\u7b2c\d+\u9898'))  # //*[@id="practise__wrap"]/div[2]/div[2]/text()[1]
        # print(len(elm))

        # print(bsObj.find('div',id='123').get_text())
        try:
            # print(len(elm) )
            if len(elm) == 1:
                #print('OK begin')
                break
        except:
            #print('EXCEPT')
            pass

    return elm.get_text()

if __name__ =='__main__':



    list_link = 'http://bitland.21tb.com/wx/checkLogin.do?functionName=raceInfo&wxType=SUBSCRIBE&raceId=1d719d0f5ba24541a9e55e0ed6912f47'
    opts = Options()
    # 设置chrome浏览器无界面模式
    # opts.add_argument('--headless')
    opts.add_argument('lang=en_US')
    browser = webdriver.Chrome(chrome_options=opts)
    browser.get(list_link)

    elm_h2 =get_h2_text(browser)
    elem_h2_pre = 0

    # 打开文件
    workbook = xlrd.open_workbook('d:\\answer.xls')
    sheet1 = workbook.sheet_by_name('Sheet1')
    while True:
        elm_h2 = get_h2_text(browser)
        if elem_h2_pre == elm_h2:
            continue
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH , '// *[ @ id = "QuestionWrap"] / div[1] / div / p')))
        elem = browser.find_element_by_xpath(
            '// *[ @ id = "QuestionWrap"] / div[1] / div / p')  # //*[@id="QuestionWrap"]/div[1]/div/p

        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="QuestionWrap"]/div[2]/ul')))
        elem_a = browser.find_element_by_xpath('//*[@id="QuestionWrap"]/div[2]/ul')  # //*[@id="QuestionWrap"]/div[2]/ul



        sub_elem = elem_a.find_elements_by_tag_name('li')



        #print(sheet1.col_values(0))
        if elem.text in sheet1.col_values(0):
            elem_index = sheet1.col_values(0).index(elem.text)
            #print("IN")
            for sub in sub_elem:

                elem = browser.find_element_by_xpath(
                    '// *[ @ id = "QuestionWrap"] / div[1] / div / p')  # //*[@id="QuestionWrap"]/div[1]/div/p

                WebDriverWait(browser, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="QuestionWrap"]/div[2]/ul')))
                elem_a = browser.find_element_by_xpath(
                    '//*[@id="QuestionWrap"]/div[2]/ul')  # //*[@id="QuestionWrap"]/div[2]/ul
                # print(elem)
                sub_elem = elem_a.find_elements_by_tag_name('li')

                #print(sub.find_element_by_tag_name('span').text, sheet1.cell(elem_index, 1).value)
                if  sub.find_element_by_tag_name('span').text == sheet1.cell(elem_index, 1).value:
                    #print('xxxxx',re.findall('\d+',elm_h2)[0])
                    #if re.findall('\d+',elm_h2)[0] == '22':
                        #print("Yes you can control")
                        #while True:
                           # pass

                    ActionChains(browser).move_to_element(sub)  # 移动到element
                    ActionChains(browser).click(sub).perform()  # 点击
                    #print(elem_h2_pre, elm_h2)
                    elem_h2_pre = elm_h2
                    #time.sleep(4)
                    break
        else:
            #print('Q', elem.text)
            #print('OUt')
            workbooknew = copy(workbook)
            ws = workbooknew.get_sheet(0)
            ws.write(sheet1.nrows, 0, elem.text)
            i = 0
            for sub in sub_elem:
                i=i+1
                try:
                    pass
                    # print(browser.page_source)
                except:
                    pass
                print('A', sub.find_element_by_tag_name('span').text)
                ws.write(sheet1.nrows, i, sub.find_element_by_tag_name('span').text)
            #ws.write(sheet1.nrows, 2, sub_elem[1].find_element_by_tag_name('span').text)
            workbooknew.save('d:\\answer.xls')




    #element = WebDriverWait(browser, 300).until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))