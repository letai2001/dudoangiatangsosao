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




df_link = pd.read_csv('product_link_balo.csv')
p1_link = df_link['link_item'].to_list()
p_link = p1_link[602:1200]
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
        
# driver.get('https://tiki.vn/gau-bong-cho-corgi-cao-cap-memon-thu-nhoi-bong-cho-corgi-map-tron-de-thuong-mem-min-p187183184.html?itm_campaign=tiki-reco_UNK_DT_UNK_UNK_tiki-listing_UNK_p-category-mpid-listing-v1_202303190600_MD_batched_PID.187183186&itm_medium=CPC&itm_source=tiki-reco&spid=187183186')
# sleep(random.randint(8,15))
prices_list = []
discount_list = []
reivew_counts_list = []
quantity_sold_list = []
rate_shop_list = []
shop_follow_list = []
count_code_discount_list = []
ratting_point_list = []

number_of_threads = 8
threads = []

def get_data_from_link(links):
    driver = webdriver.Chrome("C:\\Users\\Admin\\Downloads\\crawlDataTraining_selenium\\chromedriver.exe" , options=chrome_options)
    for link in links:
        driver.get(link)
        sleep(random.randint(3,6))

        try:
            prices = driver.find_elements(By.CLASS_NAME , "product-price__current-price")
            if len(prices) == 0:
                prices_list.append(0)
            else: 
                for price in prices:
                    prices_list.append(price.text)
        
        except NoSuchElementException:
            print("khong tim thay element!")
            prices_list.append(0)
                
                

        try:
            discounts = driver.find_elements(By.CLASS_NAME, "product-price__discount-rate")
            if len(discounts) == 0:
                discount_list.append("0")
            else:
                for discount in discounts:
                    discount_list.append(discount.text)
        except Exception as e:
            print("Khong lay duoc discount")
            discount_list.append(0)

        try:
            review_counts = driver.find_elements(By.CLASS_NAME , "number")

            if len(review_counts) == 0:
                reivew_counts_list.append(0)
            else: 
                for review_count in review_counts:
                    reivew_counts_list.append(int(review_count.text.split()[1]))
        except Exception as e:
            print("Khong lay duoc review_count")
            reivew_counts_list.append(0)
                    
        try: 
            quantity_sold = driver.find_element(By.CSS_SELECTOR, 'div[data-view-id="pdp_quantity_sold"].styles__StyledQuantitySold-sc-1u1gph7-2.exWbxD')
         
            if quantity_sold is None:
                quantity_sold_list.append(0)
                
            else: 
                sold_number = quantity_sold.get_attribute("innerText").split()[2]
                quantity_sold_list.append(sold_number)
        except Exception as e:
            print("khong thay phan tu quantitysold")
            quantity_sold_list.append(0)



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
                else:
                    rating = 0
                rate_shop_list.append(rating)
            else:
                rate_shop_list.append(0)
        except Exception as e: 
            print("khong thay phan tu item_review")
            rate_shop_list.append(0)




        
        try:
            shop_follow = driver.find_element(By.CLASS_NAME, "item.normal") 
            if shop_follow is None:
                shop_follow_list.append(0)
            else:
                try:
                    title_div = shop_follow.find_element(By.CLASS_NAME, "title")
                    span = title_div.find_element(By.TAG_NAME, "span")
                    follow_text = span.get_attribute("textContent")
                    follow = humanfriendly.parse_size(follow_text, binary=True)
                    shop_follow_list.append(follow)
                except:
                    shop_follow_list.append(0)
        except Exception as e:
            print("Khong lây dc shop_follow!")
            shop_follow_list.append(0)

        try:
            count_codes = driver.find_elements(By.CLASS_NAME, "coupon__text")

            if len(count_codes) == 0:
                count_code_discount_list.append(0)
            else:
                for count_code in count_codes:
                    try:
                        count_code_discount_list.append(int(count_code.text.split(" ")[0]))
                    except:
                        count_code_discount_list.append(0)
        except Exception as e:
            print("Khong lây dc count_code!")
            count_code_discount_list.append(0)

        
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        sleep(3)

        try:
            ratting_points = driver.find_elements(By.CLASS_NAME , "review-rating__point")
            if len(ratting_points) == 0:
                ratting_point_list.append('0')
            else:
                for ratting_point in ratting_points:
                    ratting_point_list.append(ratting_point.text)
        except Exception as e:
            print("Khong lay duoc rating_point!")
            ratting_point_list.append(0)
for i in range(number_of_threads):
    start = i * (len(p_link) // number_of_threads)
    end = (i + 1) * (len(p_link) // number_of_threads)
    if i == number_of_threads - 1:
        end = len(p_link)
    thread_links = p_link[start:end]
    t = threading.Thread(target=get_data_from_link, args=(thread_links,))
    threads.append(t)

# Bắt đầu chạy các thread
for t in threads:  
    t.start()

# Đợi cho tất cả các thread hoàn thành công việc
for t in threads:
    t.join()



print(prices_list)
print(len(prices_list))
print(discount_list)
print(len(discount_list))
print(reivew_counts_list)
print(len(reivew_counts_list))

print(quantity_sold_list)
print(len(quantity_sold_list))

print(rate_shop_list)
print(len(rate_shop_list))


print(shop_follow_list)
print(len(shop_follow_list))

print(count_code_discount_list)
print(len(count_code_discount_list))

print(ratting_point_list)
print(len(ratting_point_list))




df1 = pd.DataFrame({ 'price': prices_list , 'discount': discount_list , 'review_count': reivew_counts_list , 'quantity_sold': quantity_sold_list , 'rate_shop': rate_shop_list , 'shop_follow' : shop_follow_list , 'count_code' : count_code_discount_list , 'rating_avarage' : ratting_point_list} )

df1.to_csv('all_item_balo_602_1200.csv', index=True)
