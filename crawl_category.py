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

# def get_links():

    # Mở trang web Tiki
driver.get("https://tiki.vn/")
sleep(random.randint(2,4))

    # Tìm tất cả các đối tượng chứa link đến trang sản phẩm
title_elements = driver.find_elements(By.CLASS_NAME, 'styles__StyledItem-sc-oho8ay-0.bzmzGe')
link_elements = title_elements[8:]

    # Lưu trữ các liên kết vào danh sách
links = [link.get_attribute("href") for link in link_elements]
links = links[:-1]
df1 = pd.DataFrame({'link_category': links} )
df1.to_csv('link.csv', index=True)

    # Đóng trình duyệt

    # Trả về danh sách liên kết
# return links
