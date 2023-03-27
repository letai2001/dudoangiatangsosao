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
import json




df_link = pd.read_csv('product_link_.csv')
p_link = df_link['link_item'].to_list()
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
#git
driver = webdriver.Chrome("C:\\Users\\Admin\\Downloads\\crawlDataTraining_selenium\\chromedriver.exe" , options=chrome_options)
# driver.get('https://tiki.vn/gau-bong-cho-corgi-cao-cap-memon-thu-nhoi-bong-cho-corgi-map-tron-de-thuong-mem-min-p187183184.html?itm_campaign=tiki-reco_UNK_DT_UNK_UNK_tiki-listing_UNK_p-category-mpid-listing-v1_202303190600_MD_batched_PID.187183186&itm_medium=CPC&itm_source=tiki-reco&spid=187183186')
# sleep(random.randint(8,15))
# prices_list = []#price
# discount_list = []
# reivew_counts_list = []
# quantity_sold_list = []
# rate_shop_list = []
# shop_follow_list = []
# count_code_discount_list = []
# ratting_point_list = []
# link2 = []
# data =  []
data = []
MAX_RETRIES = 5
def find_ele(class_name):
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
        
for i in range(9 , 18):
        print("lay data trang thu "+str(i))
        a = p_link[i]
        driver.get(a)
        sleep(1.5)
        price = find_ele("product-price__current-price")
        discount = find_ele("product-price__discount-rate")
        review_count = find_ele("number")
        review_count = int(review_count.split()[1])
        count_code = find_ele("coupon__text")
        count_code = int(count_code.split(" ")[0])
        
        
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
                else:
                    try:
                        title_div = shop_follow.find_element(By.CLASS_NAME, "title")
                        span = title_div.find_element(By.TAG_NAME, "span")
                        follow_text = span.get_attribute("textContent")
                        follow = humanfriendly.parse_size(follow_text, binary=True)
                        # shop_follow_list.append(follow)
                    except:
                        follow = 0
            except Exception as e:
                print(f"Khong lây dc shop_follow , retrying ({j+1}/{MAX_RETRIES})...!")
                if(j==4):
                        follow  = 0
                sleep(1)

     

        
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        sleep(1)
        ratting_point = find_ele("review-rating__point")
      
        
        # link2.append(a)
        data.append({"link": a, "price": price,  'discount': discount , 'review_count' : review_count , "count_code": count_code , "quantity_sold": sold_number , "rate_shop": rating , "shop_follow": follow  , "rating_avarage": ratting_point })

# Ghi dữ liệu vào file JSON
        json_data = json.dumps(data)

        with open('data.json', 'a') as f:
            json.dump(data[-1], f)  # chỉ ghi phần tử mới nhất vào file
            f.write('\n')  # thêm dấu xuống dòng để phân tách các phần tử


        # try:
        #     df1 = pd.DataFrame({ 'link': link2 , 'price': prices_list , 'discount': discount_list , 'review_count': reivew_counts_list , 'quantity_sold': quantity_sold_list , 'rate_shop': rate_shop_list , 'shop_follow' : shop_follow_list , 'count_code' : count_code_discount_list , 'rating_avarage' : ratting_point_list} )
        #     df1.to_csv('data.csv', index=False)
        # # except IndexError as e:
        # #     print(f"Error occurred while processing link {link}: {e}")
        # #     df1.to_csv('data.csv', index=False)
        # except Exception as e:
        #     print(f"Error occurred while processing link {p_link[i]}: {e}")
        #     df1.to_csv('data.csv', index=False)


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

# df1.to_csv('all_item_chamsocnhacua2.csv', index=True)
