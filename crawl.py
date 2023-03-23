import numpy as np
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
import itertools

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome("C:\\Users\\Admin\\Downloads\\crawlDataTraining_selenium\\chromedriver.exe" , options=chrome_options)
# Open URL
driver.get("https://tiki.vn/giay-dep-nam/c1686")
sleep(random.randint(2,4))
links = []
prices = []
for i in range(2, 49):
    # Truy cập trang Tiki có chỉ số i
    driver.get('https://tiki.vn/giay-dep-nam/c1686?page=' + str(i))
    sleep(random.randint(1,3))
    elems = driver.find_elements(By.CLASS_NAME , "product-item")
    for elem in elems: 
        link  = elem.get_attribute('href')
        links.append(link)         
    # elems_prices = driver.find_elements(By.CSS_SELECTOR , ".price-discount__price")
    # for elem_price in elems_prices:
    #     price = elem_price.text
    #     prices.append(elem_price)
df1 = pd.DataFrame({'link_item': links} )
df1.to_csv('product_link_giaydepnam.csv', index=True)
