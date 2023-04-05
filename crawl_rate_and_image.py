import numpy as np
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
import itertools
from selenium.common.exceptions import NoSuchElementException
import re
import humanfriendly
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import threading
from queue import Queue
from crawl import TikiScraper_link_item
import json
from selenium.common.exceptions import TimeoutException
import os


df_link = pd.read_csv('links.csv')
# TSC = TikiScraper_link_item()
# df_link = TSC.scrape_page_link()

p_link = df_link['link'].to_list()
# p_link = p1_link[42:100]
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
        
# driver.get('https://tiki.vn/gau-bong-cho-corgi-cao-cap-memon-thu-nhoi-bong-cho-corgi-map-tron-de-thuong-mem-min-p187183184.html?itm_campaign=tiki-reco_UNK_DT_UNK_UNK_tiki-listing_UNK_p-category-mpid-listing-v1_202303190600_MD_batched_PID.187183186&itm_medium=CPC&itm_source=tiki-reco&spid=187183186')
# sleep(random.randint(8,15))
data = []

MAX_RETRIES = 5
number_of_threads = 12
def find_ele(driver , class_name):
    for j in range(MAX_RETRIES):
            try:
                    
                    element = driver.find_element(By.CLASS_NAME , class_name)
                    if element is not None:
                        x = element.text
                    else :
                        x  = 0
                    break   
            except Exception:
                    print(f"Element not found, retrying ({j+1}/{MAX_RETRIES})...")
                    if(j==4):
                        x = 0
                    height = driver.execute_script("return document.documentElement.scrollHeight")
                    if class_name == "review-images__heading" :
                        driver.execute_script("window.scrollBy(0, {});".format(int(height * (0.4+j*0.1))))
                    sleep(1.5*j)
    return x
lock = threading.Lock()
visited_links_lock  = threading.Lock()
visited_links = set()
# Open the JSON file for reading
def find_rating(driver , classname):
    for j in range(MAX_RETRIES+1):
            try:
                    height = driver.execute_script("return document.documentElement.scrollHeight")
                    wait = WebDriverWait(driver, 15)
                    sleep(4)
                    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, classname )))
                    if element is not None:
                        x = element.text
                    else :
                        x  = 0
                    break 
            except Exception:
                    print(f"Element rating_point_ele or image  not found, retrying ({j+1}/{MAX_RETRIES+1})...")
                    if(j==MAX_RETRIES):
                        x = 0
                   
                    driver.execute_script("window.scrollBy(0, {});".format(int(height * (0.4+j*0.1))))
                    sleep(2*j)
    return x
try:
    with open('data_fix_rate.json', 'r') as f:
        for line in f:
            obj = json.loads(line)
            visited_links.add(obj['link'])
except json.decoder.JSONDecodeError as e:
    print(f'Lỗi phân tích JSON: {e}')
def get_data_from_link(links , lock , visited_links_lock):
    driver = webdriver.Chrome("C:\\Users\\Admin\\Downloads\\crawlDataTraining_selenium\\chromedriver.exe" , options=chrome_options)
    for link in links:
       
            if link not in visited_links:
                    driver.get(link)
                    sleep(2)
                   
                    height = driver.execute_script("return document.documentElement.scrollHeight")

                        # # Cuộn trang xuống 1/3 chiều cao của trang
                    driver.execute_script("window.scrollBy(0, {});".format(int(height * 0.2)))
                        # html = driver.find_element(By.TAG_NAME, 'html')
                        # html.send_keys(Keys.END) 
                    sleep(2)
                        
                    driver.execute_script("window.scrollBy(0, {});".format(int(height * 0.25)))

                    sleep(4)
                        # driver.execute_script("window.scrollBy(0, {});".format(int(height * 0.6)))
                        # sleep(2)
                     # driver.execute_script("window.scrollBy(0, {});".format(int(height * 0.7)))
                    number_image = find_ele(driver , "review-images__heading")
                        
                        # rating_point_ele = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "review-rating__point")))
                    driver.execute_script("window.scrollTo(0, {});".format(int(height * 0.4)))
                    rating_point = find_rating(driver, "review-rating__point")
                        # x = driver.find_element(By.CLASS_NAME ,  "review-rating__point")
                   
                    

                
                    # link2.append(a)
                    # new_product = {"link": link, "price": price, 'discount': discount, 'review_count': review_count,
                    #         "count_code": count_code, "quantity_sold": sold_number, "rate_shop": rating, "shop_follow": follow,
                    #         "rating_avarage": rating_point}
                    data.append({"link": link,"number_image":number_image,"rating_avarage": rating_point})
                    
            
                    with visited_links_lock:
                        visited_links.add(link)
        # Ghi dữ liệu vào file JSON
                    with lock:
                        with open('data_fix_rate.json', 'a') as f:
                            json.dump(data[-1], f)
                            f.write('\n')

        # df = pd.DataFrame(data, columns=['Link', 'Price', 'Discount', 'Number of Ratings', 'Number of Reviews', 'Store Rating', 'Number of Store Followers', 'Available Coupons', 'Average Rating'])
        
threads = []

for i in range(number_of_threads):
    start = i * (len(p_link) // number_of_threads)
    end = (i + 1) * (len(p_link) // number_of_threads)
    if i == number_of_threads - 1:
        end = len(p_link)
    thread_links = p_link[start:end]
    t = threading.Thread(target=get_data_from_link, args=(thread_links ,lock , visited_links_lock ,))
    threads.append(t)

# Bắt đầu chạy các thread
for t in threads:  
    t.start()

# Đợi cho tất cả các thread hoàn thành công việc
for t in threads:
    t.join()
