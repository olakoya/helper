from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from time import sleep

class Automation:
    def __init__(self, browser, url, search):
        self.browser = browser
        self.url = url
        self.search = search

        # Define option here for Firefox
        option = Options()

        if self.browser == "Chrome": 
            # Use ChromeDriverManager for Chrome
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        elif self.browser == "Firefox":
            # Set Firefox binary location if needed
            option.binary_location = r'/Applications/Firefox.app/Contents/MacOS/firefox-bin'
            self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=option)
        else:
            print('Browser not found')
            self.driver = None  # Ensure driver is None if not found

        # Check if the driver was successfully initialized
        if self.driver is None:
            raise Exception("Failed to initialize the WebDriver.")

    def open_browser(self):
        if self.driver is not None:
            self.driver.get(self.url)
        else:
            print("Browser not found and Driver not initializing")

    def search_string(self):
        self.driver.implicitly_wait(10)
        if 'amazon' in self.url:
            search_field = self.driver.find_element(By.ID, 'twotabsearchtextbox')
            search_field.send_keys(self.search)
            search_field.send_keys(Keys.RETURN)
            sleep(5)
        else:
            print('Search string not found for this url')

    def close_browser(self):
        self.driver.close()

class AmazonShopping(Automation):
    def __init__(self, browser, url, search, item_to_add, email, password):
        super().__init__(browser, url, search)
        self.item_to_add = item_to_add
        self.email = email
        self.password = password

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
            if self.item_to_add in item:
                self.driver.implicitly_wait(10)
                self.driver.find_element(By.LINK_TEXT, item).click()
                sleep(10)
                break

    def add_to_cart(self):
        try:
            # Wait for the Add to Cart button to be clickable
            add_to_cart_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#a-autoid-0-announce'))  # Updated selector
            )
            add_to_cart_button.click()
            sleep(5)

            # Handle login page if prompted
            self.handle_login()

            # Wait for the confirmation message after adding to cart
            confirmation_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.h2.a-size-large'))  # Update to the actual confirmation selector
            )
            print("Item added to cart:", confirmation_message.text)

        except (TimeoutException, ElementNotInteractableException) as e:
            print(f"Error: {e}. Trying JavaScript click as fallback.")
            # Retry fetching the button if it was stale
        try:
                add_to_cart_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#a-autoid-0-announce'))
                )
                self.driver.execute_script("arguments[0].click();", add_to_cart_button)
                sleep(5)

                # Confirm item addition
                confirmation_message = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '.h2.a-size-large'))
                )
                print("Item added to cart:", confirmation_message.text)

        except Exception as inner_e:
            print(f"Fallback click also failed: {inner_e}")

        except Exception as e:
            print(f"Unhandled Exception: {e}")

    def handle_login(self):
        try:
            # Check if login page is displayed by finding the email input field
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ap_email"))
            )
            print("Login page detected. Entering credentials.")

            # Enter email
            email_field.send_keys(self.email)
            self.driver.find_element(By.ID, "continue").click()

            # Enter password
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ap_password"))
            )
            password_field.send_keys(self.password)

            # Click the login button
            self.driver.find_element(By.ID, "signInSubmit").click()

            print("Logged in successfully.")
        except TimeoutException:
            print("Login page not detected, continuing without login.")

    def close_modal_if_present(self):
        try:
            close_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.close-modal-button-selector'))  # Replace with correct selector
            )
            close_button.click()
        except TimeoutException:
            pass  # No modal found, continue as usual


# Example usage
print("Script is running!")

item = 'iPhone'
email = 'eltechsoftwaretesting@gmail.com'  # Replace with your actual email
password = 'abcdef123456@'  # Replace with your actual password
shopping_website = AmazonShopping('Chrome', 'https://www.amazon.com', item, item, email, password)
shopping_website.open_browser()
shopping_website.search_string()
shopping_website.click_product()
shopping_website.add_to_cart()
