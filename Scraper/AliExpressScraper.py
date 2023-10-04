"""
 * Author:    Andreas Naoum
 * Created:   30.09.2023
 *
 * (c) Copyright iDeal
"""

from csv import writer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from datetime import date

"""
#TODO:

- Change Currency 
- Get Shipping Cost 
- Get images

"""


class AliExpressProductFetcher:

    def __init__(self, urls, markets):
        self.urls = urls
        self.markets = markets
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    # function to extract product name
    def get_product_name(self):
        try:
            product_name = self.driver.find_element(By.XPATH, '//div[@class="title--wrap--Ms9Zv4A"]/h1').text
            # print("PRODUCT NAME:", product_name)
        except Exception as e:
            product_name = "Not available"
        return product_name

        # function to extract sale price

    def get_sale_price(self):
        try:
            sale_price = ''
            sale_price_elements = self.driver.find_elements(By.XPATH,
                                                            '//div[@class="es--wrap--erdmPRe notranslate"]/span')
            for sale_price_ele in sale_price_elements:
                sale_price_ele = sale_price_ele.text
                sale_price = sale_price + sale_price_ele
        except Exception as e:
            sale_price = "Not available"
        return sale_price

    # function to extract mrp
    def get_mrp(self):
        try:
            mrp = self.driver.find_element(By.XPATH, '//span[@class="price--originalText--Zsc6sMv"]').text
        except Exception as e:
            mrp = 'Not available'
        return mrp

    # function to extract discount
    def get_discount(self):
        try:
            discount = self.driver.find_element(By.XPATH, '//span[@class="price--discount--xET8qnP"]').text
        except Exception as e:
            discount = 'Not available'
        return discount

    # function to extract rating
    def get_rating(self):
        try:
            rating = self.driver.find_element(By.XPATH, '//span[@class="overview-rating-average"]').text
        except Exception as e:
            rating = 'Not available'
        return rating

    # function to extract number of reviews
    def get_reviews(self):
        try:
            no_of_reviews = self.driver.find_element(By.XPATH, '//a[@class="product-reviewer-reviews black-link"]').text
        except Exception as e:
            no_of_reviews = 'Not available'
        return no_of_reviews

    # function to extract seller name
    def get_seller(self):
        try:
            seller_name = self.driver.find_element(By.XPATH, '//a[@class="store-header--storeName--vINzvPw"]').text
        except Exception as e:
            seller_name = 'Not available'
        return seller_name

    """
        # wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "switcher-item"))).click()
        # // a[ @class ='switcher-item' and text()='English']
        # //a[@class='switcher-item']

        # wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select-item"))).click()
        # ship_to_australia_element = self.driver.find_element(By.XPATH,"//li[@class='switcher-item ']//span[@class='language-selector' and text()='" + "English" + "']")
        # actions.move_to_element(ship_to_australia_element).perform()

        # WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'switcher-info')]/span[@class='ship-to']/i"))).click()
        # WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//a[@class='address-select-trigger']//span[@class='css_flag css_in']//span[@class='shipping-text']"))).click()
        # WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//li[@class='address-select-item ']//span[@class='shipping-text' and text()='Afghanistan']"))).click()
        # print("Country Changed!")

    """

    def change_country(self, country):
        wait = WebDriverWait(self.driver, 10)
        actions = ActionChains(self.driver)
        try:
            wait.until(
                EC.element_to_be_clickable(
                    By.XPATH, "//div[contains(@style,'display: block')]//img[contains(@src,'TB1')]"
                )
            ).click()
        except:
            pass
        try:
            wait.until(
                EC.element_to_be_clickable(
                    By.XPATH, "//img[@class='_24EHh']"
                )
            ).click()
        except:
            pass
        wait.until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "ship-to")
            )
        ).click()
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shipping-text"))).click()
        ship_to_country_element = self.driver.find_element(By.XPATH,
                                                           "//li[@class='address-select-item ']//span[@class='shipping-text' and text()='" + country + "']")
        actions.move_to_element(ship_to_country_element).perform()
        sleep(1)
        ship_to_country_element.click()
        sleep(1)
        selected_language = "Nan"
        try:
            selected_language = self.driver.find_element(
                By.XPATH,
                '//span[@class="select-item"]//a'
            ).text
            print("Selected language is ", selected_language)
        except Exception as e:
            print("Exception Language ", e)
            selected_language = 'Not available'
        if selected_language != "English":
            wait.until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "language-selector")
                )
            ).click()
            language_element = self.driver.find_element(
                By.XPATH,
                "//a[text()='English']"
            )
            actions.move_to_element(language_element).perform()
            sleep(1)
            language_element.click()
            sleep(1)
        selected_currency = "Nan"
        try:
            #     # //div[@data-role="switch-currency"]
            # selected_currency = self.driver.find_element(By.XPATH, '//div[@data-role="switch-currency"]//span[@class="select-item"]//a').text
            selected_currency = self.driver.find_element(
                By.CSS_SELECTOR,
                'div[data-role="switch-currency"].switcher-currency-c'
            ).text
            print("Selected currency is ", selected_currency)
        except Exception as e:
            print("Exception ", e)
            selected_currency = 'Nan'
        if selected_currency != "EUR ( Euro )":
            wait.until(
                EC.element_to_be_clickable(
                    By.CSS_SELECTOR, 'div[data-role="switch-currency"].switcher-currency-c'
                )
            ).click()
            # sleep(2)
            currency_element = self.driver.find_element(
                By.XPATH, "//li//a[contains(text(), 'EUR')]"
            )
            # sleep(2)
            self.driver.execute_script(
                "arguments[0].click()",
                currency_element
            )
            # currency_element = self.driver.find_element(By.XPATH, '//li//a[@data-currency="EUR"]//em[text()= " (  Euro  )"]').click()
            # sleep(1)
            # actions.move_to_element(currency_element).perform()
            # sleep(1)
            # currency_element.click()
            # sleep(1)
            # wait.until(EC.element_to_be_clickable(currency_element)).click()

        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-role='save']"))).click()

    # https://www.aliexpress.com/item/1005006032317200.html
    def fetch(self):
        file_name = 'iDeal-Products-' + str(date.today()) + '.csv'
        heading = [
            'URL',
            'Name',
            'Rating',
            '#Reviews',
            'Seller'
        ]
        for market in self.markets:
            heading.append(market + " Sale Price")
            heading.append(market + " Discount")
        print("Start writing to file")
        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            theWriter = writer(f)
            theWriter.writerow(heading)
        # Initializing web driver
        records = []
        current_record = {}
        for url in self.urls:
            self.driver.get(url)
            sleep(2)
            current_record['product_name'] = self.get_product_name()
            current_record['rating'] = self.get_rating()
            current_record['no_of_reviews'] = self.get_reviews()
            current_record['seller_name '] = self.get_seller()
            sleep(1)
            for market in self.markets:
                print('Product: ', url, ' for country: ', market, ' is fetching now.')
                sleep(2)
                self.change_country(market)
                sleep(2)
                current_record[market + "_sale_price"] = self.get_sale_price()
                current_record[market + "_discount"] = self.get_discount()
            with open(file_name, 'a', newline='', encoding='utf-8') as f:
                theWriter = writer(f)
                row = [
                    url,
                    current_record['product_name'],
                    current_record['rating'],
                    current_record['no_of_reviews'],
                    current_record['seller_name'],
                ]
                for market in self.markets:
                    row.append(current_record[market + "_sale_price"])
                    row.append(current_record[market + "_discount"])
                theWriter.writerow(row)
            print('Product: ', current_record['product_name'], ' for country: ', current_record['market'],
                  ' is fetched.')
        # Closing the web browser
        self.driver.quit()
        return records


aliexpress_products_urls_test = [
    'https://www.aliexpress.com/item/1005006032317200.html',
    'https://www.aliexpress.com/item/1005005398972998.html'
    #    'https://www.aliexpress.com/item/1005005204880592.html',
    #    'https://www.aliexpress.com/item/1005004908957110.html',
    #    'https://www.aliexpress.com/item/1005005044624752.html'
]

markets = [
    "Bulgaria",
    "Austria",
    #    "France",
    "Belgium",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Estonia",
    "Finland",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    #    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    #    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    #    "Slovakia",
    "Slovenia",
    #    "Spain",
    "Sweden"
]

if __name__ == '__main__':
    fetcher = AliExpressProductFetcher(aliexpress_products_urls_test, markets)
    products_catalogue = fetcher.fetch()
    print("Products are fetched!")
    # print(my_dict)
    # Opening a CSV file
    file_name = 'iDeal-Products-' + str(date.today()) + '.csv'
    print('File: ', file_name, ' is written.')
