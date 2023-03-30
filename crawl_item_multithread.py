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



df_link = pd.read_csv('link_fix_rep.csv')
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
number_of_threads = 8
def find_ele(driver , class_name):
    for j in range(MAX_RETRIES):
            try:
                    x = driver.find_element(By.CLASS_NAME , class_name)
                    if x is not None:
                        x = x.text
                    else :
                        x  = 0
                    break   
            except Exception:
                    print(f"Element not found, retrying ({j+1}/{MAX_RETRIES})...")
                    if(j==4):
                        x = 0
                    sleep(1.5*j)
    return x
lock = threading.Lock()
visited_links_lock  = threading.Lock()
visited_links = set()
# Open the JSON file for reading


try:
    with open('data_fix.json', 'r') as f:
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
                    price = find_ele(driver , "product-price__current-price")
                    discount = find_ele(driver , "product-price__discount-rate")
                    review_count = find_ele(driver , "number")
                    # review_count = int(review_count.split()[1])
                    count_code = find_ele(driver , "coupon__text")
                # count_code = int(count_code.split(" ")[0])
                
                
                    sold_number = 0
                    for j in range(MAX_RETRIES):            
                        try: 
                            quantity_sold = driver.find_element(By.CSS_SELECTOR, 'div[data-view-id="pdp_quantity_sold"].styles__StyledQuantitySold-sc-1u1gph7-2.exWbxD')
                        
                            if quantity_sold is not None:
                                sold_number = quantity_sold.get_attribute("innerText").split()[2]
                                break  # thoát vòng lặp nếu đã xác định được giá trị của biến
                        except Exception as e:
                            print(f"khong thay phan tu quantitysold , retrying ({j+1}/{MAX_RETRIES})...")
                            sleep(1)


                    #rate_shop
                    rating = 0
                    
                    for j in range(MAX_RETRIES): 
                        try:
                            item_review_elements = driver.find_elements(By.CLASS_NAME, "item.review")
                            if item_review_elements:
                                item_review = item_review_elements[0]
                                title_div = item_review.find_element(By.CLASS_NAME, "title")
                                span = title_div.find_element(By.TAG_NAME, "span")
                                rating_text = span.get_attribute("textContent")
                                match = re.search(r"\d+\.\d+", rating_text)
                                if match:
                                    rating = float(match.group())
                                break  # thoát vòng lặp nếu đã xác định được giá trị của biến
                            else:
                                break  # thoát vòng lặp nếu không tìm thấy phần tử
                        except Exception as e: 
                            print(f"khong thay phan tu item_review , retrying ({j+1}/{MAX_RETRIES})...")
                            sleep(1)
                
                    




                    for j in range(MAX_RETRIES): 
                        try:
                            shop_follow = driver.find_element(By.CLASS_NAME, "item.normal") 
                            if shop_follow is None:
                                follow = 0
                                break
                            else:
                                try:
                                    title_div = shop_follow.find_element(By.CLASS_NAME, "title")
                                    span = title_div.find_element(By.TAG_NAME, "span")
                                    follow_text = span.get_attribute("textContent")
                                    follow = humanfriendly.parse_size(follow_text, binary=True)
                                    # shop_follow_list.append(follow)
                                except:
                                    follow = 0
                                break  # thoát vòng lặp nếu đã xác định được giá trị của bi
                        except Exception as e:
                            print(f"Khong lây dc shop_follow , retrying ({j+1}/{MAX_RETRIES})...!")
                            if(j==4):
                                    follow  = 0
                            sleep(1)

                    #rep_chat
                    for j in range(MAX_RETRIES): 
                        try:
                            rep_chat_ele = driver.find_element(By.CLASS_NAME, "item.chat") 
                            if rep_chat_ele is None:
                                rep_chat_text = "N/A"
                            else:
                                try:
                                    title_div = rep_chat_ele.find_element(By.CLASS_NAME, "title")
                                    span = title_div.find_element(By.TAG_NAME, "span")
                                    rep_chat_text = span.get_attribute("textContent")
                                    break
                                    # shop_follow_list.append(follow)
                                except:
                                    rep_chat_text = "N/A"
                                    break
                        except Exception as e:
                            print(f"Khong lây dc rep_chat , retrying ({j+1}/{MAX_RETRIES})...!")
                            if(j==4):
                                    rep_chat_text = "N/A"
                            sleep(1)
                    

                    


                    
                    
                    try:
                        height = driver.execute_script("return document.documentElement.scrollHeight")

                        # # Cuộn trang xuống 1/3 chiều cao của trang
                        driver.execute_script("window.scrollBy(0, {});".format(int(height * 0.2)))
                        # html = driver.find_element(By.TAG_NAME, 'html')
                        # html.send_keys(Keys.END) 
                        sleep(2)
                        
                        driver.execute_script("window.scrollBy(0, {});".format(int(height * 0.4)))

                        sleep(2)
                        driver.execute_script("window.scrollBy(0, {});".format(int(height * 0.6)))
                        number_image = find_ele(driver , "review-images__heading")
                        wait = WebDriverWait(driver, 20)
                        sleep(4)
                        rating_point_ele = wait.until(lambda ele_rating_point: driver.find_element(By.CLASS_NAME ,  "review-rating__point"))
                        rating_point = rating_point_ele.text
                        # x = driver.find_element(By.CLASS_NAME ,  "review-rating__point")
                    except TimeoutException:
                        print("Element not found within 20 seconds")
                        rating_point = 0
                
                    # Check if JSON file exists and is not empty
                    

                    

                    
                    # link2.append(a)
                    # new_product = {"link": link, "price": price, 'discount': discount, 'review_count': review_count,
                    #         "count_code": count_code, "quantity_sold": sold_number, "rate_shop": rating, "shop_follow": follow,
                    #         "rating_avarage": rating_point}
                    data.append({"link": link, "price": price, 'discount': discount, 'review_count': review_count,
                            "count_code": count_code, "quantity_sold": sold_number, "rate_shop": rating, "shop_follow": follow, "rep_chat":rep_chat_text , "number_image":number_image,
                            "rating_avarage": rating_point})
                    
            
                    with visited_links_lock:
                        visited_links.add(link)
        # Ghi dữ liệu vào file JSON
                    with lock:
                        with open('data_fix.json', 'a') as f:
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



# print(prices_list)
# print(len(prices_list))
# print(discount_list)
# print(len(discount_list))
# print(reivew_counts_list)
# print(len(reivew_counts_list))

# print(quantity_sold_list)
# print(len(quantity_sold_list))

# print(rate_shop_list)
# print(len(rate_shop_list))


# print(shop_follow_list)
# print(len(shop_follow_list))

# print(count_code_discount_list)
# print(len(count_code_discount_list))

# print(ratting_point_list)
# print(len(ratting_point_list))




# df1 = pd.DataFrame({ 'price': prices_list , 'discount': discount_list , 'review_count': reivew_counts_list , 'quantity_sold': quantity_sold_list , 'rate_shop': rate_shop_list , 'shop_follow' : shop_follow_list , 'count_code' : count_code_discount_list , 'rating_avarage' : ratting_point_list} )

# df1.to_csv('all_item_balo_602_1200.csv', index=True)
