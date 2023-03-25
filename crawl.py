import numpy as np
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
import itertools
from crawl_category import TikiScraper
import threading

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')

# Open URL
# driver.get("https://tiki.vn/balo-va-vali/c6000")
# sleep(random.randint(2,4))
# Khởi tạo đối tượng scraper
scraper = TikiScraper()

# Lấy danh sách liên kết
links = scraper.get_links()

link_item = []
MAX_RETRIES = 5
def scrape_page(links):
    driver = webdriver.Chrome("C:\\Users\\Admin\\Downloads\\crawlDataTraining_selenium\\chromedriver.exe" , options=chrome_options)

    for link in links:
        for i in range(2, 49):
                # Truy cập trang Tiki có chỉ số i
                    driver.get(link + '?page='+ str(i))
                    sleep(random.randint(1,3))
                    
                    for i in range(MAX_RETRIES):
                    
                        try:
                            elems = driver.find_elements(By.CLASS_NAME , "product-item")
                            break
                        except NoSuchElementException:
                            print(f"Element not found, retrying ({i+1}/{MAX_RETRIES})...")
                            sleep(1)

                    
                    for elem in elems:
                        for i in range(MAX_RETRIES):
                            try: 
                                link2  = elem.get_attribute('href')
                                link_item.append(link2)
                                break
                            except:
                                print("khong thay href!")
                                sleep(1)
                           
        # elems_prices = driver.find_elements(By.CSS_SELECTOR , ".price-discount__price")
        # for elem_price in elems_prices:
        #     price = elem_price.text
        #     prices.append(elem_price)
threads = []
number_of_threads = 8
for i in range(number_of_threads):
    start = i * (len(links) // number_of_threads)
    end = (i + 1) * (len(links) // number_of_threads)
    if i == number_of_threads - 1:
        end = len(links)
    thread_links = links[start:end]
    t = threading.Thread(target=scrape_page, args=(thread_links,))
    threads.append(t)

# Bắt đầu chạy các thread
for t in threads:  
    t.start()

# Đợi cho tất cả các thread hoàn thành công việc
for t in threads:
    t.join()

df1 = pd.DataFrame({'link_item': link_item} )
df1.to_csv('product_link.csv', index=True)
