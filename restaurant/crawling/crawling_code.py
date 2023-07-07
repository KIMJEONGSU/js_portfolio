from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import time
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

host = 'cluster0.w3ampdj.mongodb.net'
user = 'test'
password = '1234'
database_name = 'test_db'
collection_name = 'food_info'

client = f"mongodb+srv://{user}:{password}@{host}/{database_name}?retryWrites=true&w=majority"
data = client[database_name][collection_name]

# 크롤링한 데이터를 리스트에 추가할 예정.

# 크롤링함수
def crawling_data():
    crawling = []

    FILEPATH = os.path.join(os.getcwd(), 'chromedriver_win32')
    driver = webdriver.Chrome(FILEPATH)
    url = 'https://map.kakao.com/'
    driver.get(url)

    time.sleep(3)

    # 음식점 이름
    name_list = []
    tmp_name = driver.find_elements(By.CSS_SELECTOR, '#contents_list ul > li > div > figure > figcaption > div > span > a > h3')
    for tmp in tmp_name:
        res_name = tmp.text
        name_list.append(res_name)

    # 음식점 주소
    address_list = []
    tmp_address = driver.find_elements(By.CSS_SELECTOR, '#contents_list > ul > li > div > figure > figcaption > div > p')
    for tmp in tmp_address:
        address = tmp.text
        address_list.append(address)

    # 음식점 별점
    stars_list = []
    tmp_stars = driver.find_elements(By.CSS_SELECTOR, '#contents_list > ul > li:nth-child(1) > div > figure > figcaption > div > strong > span')
    for tmp in tmp_stars:
        stars = tmp.text
        stars_list.append(stars)

    # 더보기클릭하여 모든 맛집 리스트 보여지게 하기.
    while True:
        button = driver.find_element(By.CLASS_NAME, "more_btn")
        button.click()
        time.sleep(3)



    crawling_rows = {'음식점이름':res_name}
    crawling.append(crawling_rows)
    


    return 0

data.insert_many(crawling_data)