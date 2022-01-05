import csv,os
import time
from bs4 import BeautifulSoup
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.chrome.options import Options


def get_url(search_term):
    ''' 根据输入的关键词生成 目标网址 '''
    template = 'https://amazon.com/s?k={}&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ', '+')

    url = template.format(search_term)
    url += '&page={}'
    return url


def extract_record(item):
    ''' 从每条记录当中获取筛选信息 '''

    # 商品描述和url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')
    try:
        # 价格
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return
    # 排名
    try:
        rating = item.find('span', {'class': 'a-icon-alt'}).text
        rating = rating.split(' ')[0]
    except:
        rating = ''
    # 评价数量
    try:
        review_count = item.select_one(
            'span.a-size-base.a-color-base.s-underline-text').text
    except:
        review_count = ''

    result = {"description": description,
              "price": price, "rating": rating, "review_count": review_count, "url": url}

    return result


''' url = get_url("airipod case")
browser.maximize_window()
browser.get(url)

soup = BeautifulSoup(browser.page_source, 'html.parser')
results = soup.find_all('div', {'data-component-type': 's-search-result'})
records = []

print(len(result))
for item in result:
    record = extract_record(item)
    if record:
        records.append(record)

'''


def main(search_term, total_page, savePath,headless):
    
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2
        }
    }
    options.add_experimental_option('prefs', prefs)
    if (headless == True) or (headless >=1) :
        options.add_argument('headless')
    else:
        pass
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # executable_path="D:/Program Files/Python/python36/Lib/site-packages/chromedriver.exe"
    browser = webdriver.Chrome(
        options=options,executable_path='tool/chromedriver.exe')  # options=options
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
    """
    })
    wait = WebDriverWait(browser, 30)
    driver = browser
    records = []
    url = get_url(search_term)

    for page in range(1, total_page+1):
        print(url.format(page))
        driver.switch_to.window(driver.window_handles[0])
        driver.get(url.format(page))
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'a-pagination')))
        time.sleep(3.5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all(
            'div', {'data-component-type': 's-search-result'})

        tempUrlList = []
        for item in results:  # 调试[0:3]
            record = extract_record(item)
            if record:
                records.append(record)
                tempUrlList.append(record["url"])
                driver.execute_script(
                    "window.open('{}')".format(record["url"]))
                time.sleep(0.05)
        # print(driver.window_handles)

        for index in range(0, len(tempUrlList)):
            if index == 0:
                driver.get(tempUrlList[0])
            else:
                driver.switch_to.window(driver.window_handles[index])
            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                detail = soup.select_one('#feature-bullets > ul').text
                # item = tempUrlList[index]
                tempArr = list(filter(lambda item: item.get(
                    "url") == tempUrlList[index], records))
                tempArr[0]["detail"] = detail
                # print(records)
            except:
                tempArr = list(filter(lambda item: item.get(
                    "url") == tempUrlList[index], records))
                tempArr[0]["detail"] = ""
                pass
            # print('='*20)
        windows = driver.window_handles
        for index in range(1, len(windows)):
            try:
                driver.switch_to.window(windows[index])
                driver.close()
            except:
                pass
    print("检索完毕!")
    driver.quit()

    ''' 保存文件 '''
    
    if (savePath == None) or (savePath == ""):
        now = datetime.now()
        savePath = os.path.join(os.getcwd(),'keywords-{}.csv'.format(now.strftime("%Y-%m-%d %H-%M-%S")))
    print("保存文件中...")
    with open(savePath, 'w',encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["产品标题", "价格", "评分", "评价数量", "产品链接", "产品描述"])
        writer.writerows([record.values() for record in records])
    print("文件已保存{}".format(savePath))


def closeBrowser():
    driver = browser
    driver.quit()
# main("airpod case", 1)
# https://ahrefs.com/zh/amazon-keyword-tool
