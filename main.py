## Please read if you are going to use the script ##

## Notes : Change webdriver path to your pc's webdriver location, download the modules used in this script, and it is applicable only for Shopee Thailand ##
## Default webdriver's path: cwd/chromedriver ##

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time, re, math
import pandas as pd


## Search Page Scraping ## 
def scrape_page():

    # Name 
    shop_name = driver.find_elements_by_class_name('PFM7lj')
    for name in shop_name:
        retail_name.append(name.text)

    # market lowest possible price
    price = driver.find_elements_by_xpath('//div[@class="_1ObP5d"]/div[2]/div/span[2]')
    for prices in price:
        retail_price.append(prices.text)

    # Quantity Sold
    sold = driver.find_elements_by_class_name('go5yPW')
    for Quantity in sold:
        Quantity_Sold.append(Quantity.text)
    for i in range(len(Quantity_Sold)):
        if Quantity_Sold[i] == '':
            Quantity_Sold[i] = '0 sold'

    # Location
    Location = driver.find_elements_by_class_name('_2CWevj')
    for locate in Location:
        Retail_Location.append(locate.text)

    # Link for each item
    Link = driver.find_elements_by_xpath('//a[@data-sqe="link"]')
    for href in Link:
        links.append(href.get_attribute('href'))

    # Sleep for new URL
    time.sleep(2)


## Product Characteristics Scraping ##
def scrape_product():
 
    try:
        # rating score
        Rate = product_driver.find_element_by_xpath('//div[@class="flex flex-auto _3-GQHh"]/div[1]/div[2]/div[1]')
        rating_score.append(Rate.text)

        # rating counts
        rating_c = product_driver.find_elements_by_xpath('//div[@class="flex _21hHOx"]/div[2]/div[1]')
        for rates in rating_c:
            rating_count.append(rates.text)

        # favourite counts
        favorite1 = product_driver.find_elements_by_xpath("//div[@class='flex items-center _3nBAy8']")
        for favor in favorite1:
            if 'k' or '.' not in favor.text:
                fovar = re.findall('[0-9]+', favor.text)
                fav_count.append(fovar[0])
            elif 'k' or '.' in favor.text:
                fovar = re.findall('[0-9].+[^()]', favor.text)
                fav_count.append(fovar[0])

        sname = product_driver.find_element_by_class_name("_3uf2ae")
        shop_name.append(sname.text)

        # shop rating
        srating = product_driver.find_element_by_xpath("//div[@class='_309kqV']/div[1]/div/span")
        shop_rating.append(srating.text)

        # shop responserate
        sresponse = product_driver.find_element_by_xpath("//div[@class='_309kqV']/div[2]/div/span")
        shop_responserate.append(sresponse.text)

        # shop responsetime
        srestime = product_driver.find_element_by_xpath("//div[@class='_309kqV']/div[2]/div[2]/span")
        shop_responsetime.append(srestime.text)

        # shop followers
        follower = product_driver.find_element_by_xpath("//div[@class='_309kqV']/div[3]/div[2]/span")
        shop_follower.append(follower.text)

        # shop product variation
        product_variation = product_driver.find_element_by_xpath('//a[@class="-ilx8l _2vJ9tj"]/span')
        shop_product_variation.append(product_variation.text)

        joined = product_driver.find_element_by_xpath('//div[@class="_309kqV"]/div[3]/div[1]/span')
        shop_joined.append(joined.text)

    except NoSuchElementException:
        rating_score.append('No Rating Score On This Product')
        rating_count.append('No Rating Count On This Product')
        fav_count.append('No Favourite Count On This Product')
        shop_name.append('No Shop On This Product')
        shop_rating.append('No Shop Ratings On This Product')
        shop_responserate.append('No Shop Response Rate On This Product')
        shop_responsetime.append('No Shop Response Time On This Product')
        shop_follower.append('No Shop Followes On This Product')
        shop_product_variation.append('No Shop Product Variation On This Product')
        shop_joined.append('No Joined Date On This Product')

   # Product comments
    try:
        number_in_comment = product_driver.find_element_by_xpath('//div[@class="product-rating-overview"]/div[2]/div[7]')
        if 'k' not in number_in_comment.text:
            number_for_withcomment = number_in_comment.text + str('"]')
            number_for_withcomment = str(re.findall('.[0-9].+', number_for_withcomment)[0])
            number = int(re.findall('[0-9]+', number_for_withcomment)[0])
            if number / 6 == 0:
                next_comment = 0
            elif number / 6 <= 1:
                next_comment = math.floor(number/6) + 1
            elif 0 < number % 6 <=6:
                next_comment = math.floor(number/6)
            elif number % 6 == 0:
                next_comment = int(number/6)
        
        elif 'k' and '.' in number_in_comment.text:
            number_for_withcomment = number_in_comment.text + str('"]')
            number_for_withcomment = str(re.findall('.[0-9].+', number_for_withcomment)[0])
            number = float(re.findall('([0-9].+[0-9])', number_in_comment.text)[0])
            number = int(number * 1000)
            next_comment = math.floor(number/6)
            
        elif 'k' in number_in_comment.text:
            number_for_withcomment = number_in_comment.text + str('"]')
            number_for_withcomment = str(re.findall('.[0-9].+', number_for_withcomment)[0])
            number = int(re.findall('[0-9]+', number_in_comment.text)[0])
            number = int(number * 1000)
            next_comment = math.floor(number/6)

        withcomment = product_driver.find_element_by_xpath('//div[@class="product-rating-overview__filters"]/div[text()="with comments ' + str(number_for_withcomment))
        withcomment.click()

        all_comment = []
        if next_comment > 0:
            for iteration in range(next_comment):
                time.sleep(5)
                comments = product_driver.find_elements_by_class_name("shopee-product-rating__content")
                for comment_on_products in comments:
                    all_comment.append(comment_on_products.text)
                
                try:
                    next_comment_number = []
                    next_button_comment = product_driver.find_elements_by_xpath('//div[@class="product-ratings__list"]/div[2]/button')
                    for next_button in next_button_comment:
                        next_comment_number.append(next_button.tag_name)
                    next_comment_iteration = str([len(next_comment_number)])
                    time.sleep(1)
                    next_press = product_driver.find_element_by_xpath('//div[@class="shopee-page-controller product-ratings__page-controller"]/button' + str(next_comment_iteration))
                    time.sleep(1)
                    next_press.click()

                except ElementClickInterceptedException:
                    next_comment_number = []
                    next_button_comment = product_driver.find_elements_by_xpath('//div[@class="product-ratings__list"]/div[2]/button')
                    for next_button in next_button_comment:
                        next_comment_number.append(next_button.tag_name)
                    next_comment_iteration = str([len(next_comment_number)])
                    time.sleep(1)
                    next_press = product_driver.find_element_by_xpath('//div[@class="shopee-page-controller product-ratings__page-controller"]/button' + str(next_comment_iteration))
                    time.sleep(1)
                    next_press.click()
            product_comments.append(all_comment)
        
        else:
            product_comments.append('No Comments On This Product')

    except NoSuchElementException:
        try:
            no_product_comment = product_driver.find_element_by_xpath('//div[@class="product-ratings"]/div[2]/div[2]')
            product_comments.append(no_product_comment.text)
        except NoSuchElementException:
            no_product_exist = product_driver.find_element_by_xpath('//div[@class="product-not-exist__text"]')
            product_comments.append(no_product_exist.text)

## Lists ##
retail_name = []
retail_price = []
Quantity_Sold = []
Retail_Location = []
links = []
rating_score = []
rating_count = []
fav_count = []
shop_name = []
shop_rating = []
shop_responserate = []
shop_responsetime = []
product_comments = []
shop_follower = []
shop_product_variation = []
shop_joined = []

## Part 1: Scrape Search Engine Webpage ##

# type in product name 
shopee_find = input('What Do you want to scrape? - ')

driver = webdriver.Chrome('./chromedriver')
driver.get('https://shopee.co.th/search?keyword=' + str(shopee_find))

time.sleep(3)

# Generate click
buttonpress = driver.find_element_by_xpath('//div[@class="language-selection__list-item"]//button[text()="English"]')
buttonpress.click()

time.sleep(3)

# Find total pages number
num_page = driver.find_element_by_xpath('//div[@class="shopee-mini-page-controller"]/div[1]/span[2]')
num_page = int(num_page.text)

# Automate Webpages
for page in range(num_page):
    driver.get('https://shopee.co.th/search?keyword=' + str(shopee_find) + '&page=' + str(page))
    # Sleep
    time.sleep(1)

    # Scrolling web
    scroll_pause_time = 1
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script('window.scrollTo(0, window.scrollY + 500);')
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script('return document.body.scrollHeight')
    
        if new_height == last_height:
            driver.execute_script('window.scrollTo(0, window.scrollY + 500)')
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            else:
                last_height = new_height
                continue
    
    scrape_page()
driver.close()


## Part 2: Scrape Product Characteristics ##
product_driver = webdriver.Chrome('./chromedriver')

# Automate Product Links
for i in range(len(links)):
    product_driver.get(links[i])

    time.sleep(2)        

    # Press English Button
    try:
        EngButton = product_driver.find_element_by_xpath('//div[@class="language-selection__list-item"]//button[text()="English"]')
        EngButton.click()

        # wait for web to load after press button
        time.sleep(3)

        # Scoll html
        pause_time = 2
        while True:
            
            # Get the height of page
            last_height = product_driver.execute_script("return document.body.scrollHeight")
            product_driver.execute_script('window.scrollTo(0, window.scrollY + 500);')
            time.sleep(pause_time)
            
            # Calculate new height
            new_height = product_driver.execute_script('return document.body.scrollHeight')
            
            if new_height == last_height:
                product_driver.execute_script('window.scrollTo(0, window.scrollY + 500);')
                time.sleep(pause_time)
                new_height = product_driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    continue

        while True:

            # Get the height of page
            last_height = product_driver.execute_script("return document.body.scrollHeight")
            product_driver.execute_script('window.scrollTo(0, window.scrollY + 750);')
            time.sleep(pause_time)

            # Calculate new height
            new_height = product_driver.execute_script('return document.body.scrollHeight')
            
            if new_height == last_height:
                product_driver.execute_script('window.scrollTo(0, window.scrollY + 750);')
                time.sleep(pause_time)
                new_height = product_driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    continue
        
        while True:

            # Get the height of page
            last_height = product_driver.execute_script("return document.body.scrollHeight")
            product_driver.execute_script('window.scrollTo(0, window.scrollY + 750);')
            time.sleep(pause_time)

            # Calculate new height
            new_height = product_driver.execute_script('return document.body.scrollHeight')
            
            if new_height == last_height:
                product_driver.execute_script('window.scrollTo(0, window.scrollY + 750);')
                time.sleep(pause_time)
                new_height = product_driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    continue

        scrape_product()

    except NoSuchElementException:

        # wait for web to load after press button
        time.sleep(3)

        # Scoll html
        pause_time = 2
        while True:
            # Get the height of page
            last_height = product_driver.execute_script("return document.body.scrollHeight")
            product_driver.execute_script('window.scrollTo(0, window.scrollY + 500);')
            time.sleep(pause_time)

            # Calculate new height
            new_height = product_driver.execute_script('return document.body.scrollHeight')
            
            if new_height == last_height:
                product_driver.execute_script('window.scrollTo(0, window.scrollY + 500);')
                time.sleep(pause_time)
                new_height = product_driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    continue
        while True:
            # Get the height of page
            last_height = product_driver.execute_script("return document.body.scrollHeight")
            product_driver.execute_script('window.scrollTo(0, window.scrollY + 750);')
            time.sleep(pause_time)

            # Calculate new height
            new_height = product_driver.execute_script('return document.body.scrollHeight')
            
            if new_height == last_height:
                product_driver.execute_script('window.scrollTo(0, window.scrollY + 750);')
                time.sleep(pause_time)
                new_height = product_driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    continue
       
        while True:
        # Get the height of page
            last_height = product_driver.execute_script("return document.body.scrollHeight")
            product_driver.execute_script('window.scrollTo(0, window.scrollY + 750);')
            time.sleep(pause_time)

            # Calculate new height
            new_height = product_driver.execute_script('return document.body.scrollHeight')
            
            if new_height == last_height:
                product_driver.execute_script('window.scrollTo(0, window.scrollY + 750);')
                time.sleep(pause_time)
                new_height = product_driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    continue

        scrape_product()
product_driver.close()


## Part 3: Scrape Shop's Score ##
shop_rating_score = []
shop_driver = webdriver.Chrome('./chromedriver')
for shopeename in shop_name:

    if shopeename == 'No Shop On This Product':
        shop_rating_score.append('Shop Does Not Exist')

    elif shopeename == shopeename:
        shop_driver.get('https://shopee.co.th/' + shopeename)
        time.sleep(3)

        try:
            EngButton =shop_driver.find_element_by_xpath('//div[@class="language-selection__list-item"]//button[text()="English"]')
            EngButton.click()
            
            try:
                shopee_shop_rating_score = shop_driver.find_element_by_xpath('//div[@class="section-seller-overview-horizontal__seller-info-list"]/div[5]/div[2]/div[2]')
                shop_rating_score.append(shopee_shop_rating_score.text)
                
            except NoSuchElementException:
                shopee_shop_rating_score = shop_driver.find_element_by_xpath('//div[@class="b2c-shop-statistic__value"]')
                shop_rating_score.append(shopee_shop_rating_score.text)

        except NoSuchElementException:
            time.sleep(3)
            
            try:
                shopee_shop_rating_score = shop_driver.find_element_by_xpath('//div[@class="section-seller-overview-horizontal__seller-info-list"]/div[5]/div[2]/div[2]')
                shop_rating_score.append(shopee_shop_rating_score.text)
                
            except NoSuchElementException:
                shopee_shop_rating_score = shop_driver.find_element_by_xpath('//div[@class="b2c-shop-statistic__value"]')
                shop_rating_score.append(shopee_shop_rating_score.text)

shop_driver.close()


## Create .csv file ##
df_shopee = pd.DataFrame(
    {
        "Shop_Name": shop_name,
        "Shop_Rating_Counts": shop_rating,
        "Shop_Score": shop_rating_score,
        "Shop_Followers": shop_follower,
        "Shop_Product_Variation": shop_product_variation,
        "Shop_Response_Rate": shop_responserate,
        "Shop_Response_time": shop_responsetime,
        "Shop_Location": Retail_Location,
        "Shop_Joined": shop_joined,
        "Product_Name": retail_name,
        "Product_Price": retail_price,
        "Quantity_Sold": Quantity_Sold,
        "Product_Score": rating_score,
        "Product_Rating_Counts": rating_count,
        "Product_Favourite_Counts_by_User": fav_count,
        "Product_Comments": product_comments,
        "Links": links
        }
    )
df_shopee.to_csv('shopee_data.csv', index = False, encoding = 'utf-8')

## If there are any mistakes, please let me know. Hope you like it, thank you ##