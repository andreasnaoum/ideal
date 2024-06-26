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

from Scraper.Extractor import AliExpressLinkExtractor
import logging

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

    def get_shipping(self):
        try:
            shipping = self.driver.find_element(By.XPATH, "//span/strong[text()='Free Shipping']").text
            shipping = 'Free'
        except Exception as e:
            try:
                shipping = self.driver.find_element(By.XPATH, "//span/strong[contains(text(), 'Shipping')]").text
                shipping_partitions = shipping.partition("Shipping: ")
                shipping = shipping_partitions[2]
            except Exception as e:
                shipping = 'Nan'
        return shipping

    def get_estimate_shipping_day(self):
        try:
            date = self.driver.find_element(By.XPATH,
                                            "//div[@class='dynamic-shipping-line dynamic-shipping-contentLayout']/span/span[2]").text
        except Exception as e:
            date = 'Not available'
        return date

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


    def newHeader(self, country, wait):
        try:
            sleep(1)
            elements = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="select--arrow--1cha40Y"]'))
            )
            elements[0].click()
            element = self.driver.find_element(
                By.XPATH,
                '//div[@class="select--item--32FADYB"]//span[text()="' + country + '"]'
            )
            self.driver.execute_script(
                "arguments[0].click()",
                element
            )
            sleep(1)
            logging.debug("Country changed!")
            selected_language_element = self.driver.find_elements(
                By.XPATH,
                '//div[@class="select--text--1b85oDo"]//span[text()="English"]'
            )
            if selected_language_element:
                selected_language = selected_language_element[0].text
            else:
                selected_language = 'Nan'
            if selected_language != "English":
                logging.debug("Its time for language")
                elements[1].click()
                logging.debug("Selector pressed ")
                language_element = self.driver.find_element(
                    By.XPATH,
                    '//div[@class="select--item--32FADYB" and text()="English"]'
                )
                logging.debug("Element found")
                self.driver.execute_script(
                    "arguments[0].click()",
                    language_element
                )
            logging.debug("Language is selected")
            sleep(1)
            selected_currency_element = self.driver.find_elements(
                By.XPATH,
                '//div[@class="select--text--1b85oDo"]//span[text()="EUR ( Euro )"]'
            )
            if selected_currency_element:
                logging.debug("Selected currency element exists")
                selected_currency = "EUR ( Euro )"
            else:
                logging.debug("Selected currency element does not exists")
                selected_currency = 'Nan'
            logging.debug("Currency is ", selected_currency)
            if selected_currency != "EUR ( Euro )":
                elements[2].click()
                currency_element = self.driver.find_element(
                    By.XPATH,
                    '//div[@class="select--item--32FADYB" and text()="EUR ( Euro )"]'
                )
                self.driver.execute_script(
                    "arguments[0].click()",
                    currency_element
                )
            logging.debug("Currency is selected")
            sleep(1)
            save_button = self.driver.find_element(
                By.XPATH,
                '//div[@class="es--saveBtn--w8EuBuy"]'
            )
            self.driver.execute_script(
                "arguments[0].click()",
                save_button
            )
        except Exception as e:
            logging.error("Error in change country: ", country, ' error: ', str(e))
            pass

    def oldHeader(self, country, wait, actions):
        try:
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//img[@class='_24EHh']")
                )
            ).click()
            wait.until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "ship-to")
                )
            ).click()
            wait.until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "shipping-text")
                )
            ).click()
            sleep(1)
            ship_to_country_element = self.driver.find_element(
                By.XPATH,
                "//li[@class='address-select-item ']//span[@class='shipping-text' and text()='" + country + "']"
            )
            actions.move_to_element(
                ship_to_country_element
            ).perform()
            sleep(1)
            ship_to_country_element.click()
            sleep(1)
            selected_language = "Nan"
            try:
                selected_language = self.driver.find_element(
                    By.XPATH,
                    '//span[@class="select-item"]//a'
                ).text
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
                try:
                    selected_currency = self.driver.find_element(
                        By.CSS_SELECTOR,
                        'div[data-role="switch-currency"].switcher-currency-c'
                    ).text
                except Exception as e:
                    selected_currency = "Nan"
                    logging.error("Exception Currency: ", e)
                    selected_currency = 'Nan'
                if selected_currency != "EUR ( Euro )":
                    wait.until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, 'div[data-role="switch-currency"].switcher-currency-c')
                        )
                    ).click()
                    currency_element = self.driver.find_element(
                        By.XPATH,
                        "//li//a[contains(text(), 'EUR')]"
                    )
                    # sleep(2)
                    self.driver.execute_script(
                        "arguments[0].click()",
                        currency_element
                    )
                wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@data-role='save']")
                    )
                ).click()
                wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@data-role='save']")
                    )
                ).click()
        except Exception as e:
            print("Error in change country: ", country, ' error: ', str(e))
            pass

    def change_country(self, country):
        wait = WebDriverWait(self.driver, 2)
        actions = ActionChains(self.driver)
        try:
            wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        'span[class="comet-icon comet-icon-chevrondown32 ship-to--centerIcon--1viVSdj base--chevronIcon--25sHdop"]')
                    )
                ).click()
            self.newHeader(country, wait)
        except Exception as e:
            self.oldHeader(country, wait, actions)

    # https://www.aliexpress.com/item/1005006032317200.html
    def fetch(self):
        file_name = 'iDeal-Products-' + str(date.today()) + '.csv'
        heading = [
            'URL',
            'Name',
            'Rating',
            'No. Reviews',
            'Seller'
        ]
        for market in self.markets:
            heading.append(market + " Sale Price")
            heading.append(market + " Discount")
            heading.append(market + " Shipping")
            heading.append(market + " Shipping Date Estimation")
        print("Start writing to file")
        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            theWriter = writer(f)
            theWriter.writerow(heading)
        # Initializing web driver
        # records = []
        for url in self.urls:
            current_record = {}
            self.driver.get(url)
            sleep(2)
            current_record['product_name'] = self.get_product_name()
            # sleep(1)
            current_record['rating'] = self.get_rating()
            # sleep(1)
            current_record['no_of_reviews'] = self.get_reviews()
            # sleep(1)
            current_record['seller_name'] = self.get_seller()
            # sleep(1)
            for market in self.markets:
                print('Product: ', url, ' for country: ', market, ' is fetching now.')
                # sleep(2)
                self.change_country(market)
                sleep(3)
                current_record[market + "_sale_price"] = self.get_sale_price()
                # sleep(1)
                current_record[market + "_discount"] = self.get_discount()
                # sleep(1)
                current_record[market + "_shipping"] = self.get_shipping()
                # sleep(1)
                # print("Shipping is ", current_record[market + "_shipping"])
                if current_record[market + "_shipping"] != "Nan":
                    current_record[market + "_shipping_day"] = self.get_estimate_shipping_day()
                    # sleep(1)
                    # logging.debug("Shipping is ", current_record[market + "_shipping_day"])
                else:
                    current_record[market + "_shipping_day"] = "Nan"

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
                    row.append(current_record[market + "_shipping"])
                    row.append(current_record[market + "_shipping_day"])
                theWriter.writerow(row)
            print('Product: ', current_record['product_name'], ' is fetched.')
        # Closing the web browser
        self.driver.quit()
        # return records


aliexpress_products_urls_test = [
    'https://www.aliexpress.com/item/1005005135962246.html',
    'https://www.aliexpress.com/item/1005006032317200.html',
    'https://www.aliexpress.com/item/1005005398972998.html'
    #    'https://www.aliexpress.com/item/1005005204880592.html',
    #    'https://www.aliexpress.com/item/1005004908957110.html',
    #    'https://www.aliexpress.com/item/1005005044624752.html'
]

markets = [
    # "Bulgaria",
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
    csv_file_path = 'iDeal-AliExpress-Products-2023-10-07-CHECK.csv'
    link_extractor = AliExpressLinkExtractor(csv_file_path)
    links_array = link_extractor.extract_links()
    links_array.pop(0)
    links_array.pop(0)
    fetcher = AliExpressProductFetcher(links_array, markets)
    fetcher.fetch()
    print("Products are fetched!")
    # print(my_dict)
    # Opening a CSV file
    file_name = 'iDeal-Products-' + str(date.today()) + '.csv'
    print('File: ', file_name, ' is written.')
