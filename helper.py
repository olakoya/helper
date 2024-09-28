import os
#self.driver = webdriver.Chrome(os.environ.get('CHROMEDRIVER_PATH'))
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import options
from selenium.webdriver.firefox.options import Options
from time import sleep

#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

#search_field = WebDriverWait(self.driver, 10).until(
 #   EC.presence_of_element_located((By.ID, 'twotabsearchtextbox'))
#)


class Automation:
    def __init__(self, browser, url, search):
        self.browser = browser
        self.url = url
        self.search = search

        if self.browser == "Chrome": 
            # Use environment variable for ChromeDriver path
            self.driver = webdriver.Chrome(os.environ.get('CHROMEDRIVER_PATH')) #(r'C:\chromedriver.exe')
        elif self.browser == "Firefox":
            option = Options()
            # Use environment variable for Firefox binary location
            option.binary_location = os.environ.get('FIREFOX_BINARY_PATH', r'C:\Program Files\Mozilla Firefox\firefox.exe')#r'C:\Program Files\Mozilla Firefox\firefox.exe'
            self.driver = webdriver.Firefox(options=option, executable_path=os.environ.get('GECKODRIVER_PATH', r'C:\geckodriver.exe'))#r'C:\geckodriver.exe')
        else:
            print('Browser not found')

    def open_browser(self):
        self.driver.get(self.url) 
        #if self.browser == "Chrome":
         #   self.driver.get(self.url)
        #elif self.browser == "Firefox":
         #   self.driver.get(self.url)
        #else:
        #    print('Browser not found')

    def search_string(self):
        if 'geeksforgeeks' in self.url:
            self.driver.find_element(By.CSS_SELECTOR, '.gfg-icon_search').click()
            search_field = self.driver.find_element(By.ID, 'gcse-search-input')
            search_field.send_keys(self.search)
            search_field.send_keys(Keys.RETURN)
            sleep(5)
        elif 'amazon' in self.url:
            search_field = self.driver.find_element(By.ID, 'twotabsearchtextbox')
            search_field.send_keys(self.search)
            search_field.send_keys(Keys.RETURN)
            sleep(5)
        else:
            print('Search string not found')

    def close_browser(self):
        self.driver.close()
       # if self.browser == 'Chrome':
       #     self.driver.close()
       # elif self.browser == 'Firefox':
       #     self.driver.close()
        #else:
       #     print('Browser not found')


class AmazonShopping(Automation):
    def __init__(self, browser, url, search, item_to_add):
        super().__init__(browser, url, search)
        self.item_to_add = item_to_add

    def open_browser(self):
        super().open_browser()
        self.product_name = ""
        self.rent = ""
        self.products = ""
        self.items = []
    
    def click_product(self):
        self.products = self.driver.find_elements(By.CLASS_NAME, 's-image')
        for prod in self.products:
            self.items.append(prod.get_attribute('alt'))
        
        for item in self.items:
            self.driver.implicitly_wait(10)
            if self.item_to_add in item:
                self.driver.find_element(By.LINK_TEXT, item).click()
                sleep(10)
            else:
           
                pass

    def add_to_cart(self):
        self.driver.find_element(By.CSS_SELECTOR, r'#submit.add-to-cart').click()
        sleep(10)


print("Script is running!")

# website = Automation('Firefox', 'https://www.facebook.com', 'apple')

# website.open_browser()

# print(website.browser)
# print(website.search)
# print(website.url)