"""
 * Author:    Andreas Naoum, Zinonas Sakkas
 * Created:   30.09.2023
 * Modified:  06.10.2023
 *
 * (c) Copyright iDeal
"""
from datetime import date

import requests
import json
from ShopifyManagement.ShopifyManager import ShopifyManager
import httplib2
from bs4 import BeautifulSoup
from csv import writer

from requests_html import HTMLSession


def render_JS(URL):
    session = HTMLSession()
    r = session.get(URL)
    r.html.render()
    return r.html.text


def is_valid_aliexpress_link(id):
    try:
        if id == "None":
            return "No"
        url = 'https://www.aliexpress.com/item/' + str(id) + '.html'
        # url = 'https://www.aliexpress.com/item/11093005336910.html'
        # response = requests.get(url)
        # response.raise_for_status()  # Raise an HTTPError for bad responses
        # soup = BeautifulSoup(response.content, "html.parser")
        #
        # # Check for a specific element or message that indicates the absence of a product
        # # find_element = soup.find(string="Related items")
        # error_message_element = soup.find('div', {'class': 'item-not-found-image'})
        # if error_message_element:
        #     return "No"
        try:
            response = render_JS(url)

            soup = BeautifulSoup(response, "html.parser")

            # Check for a specific element or message that indicates the absence of a product
            find_element = soup.find(string="Related items")
            if find_element:
                return "Yes"
            # error_message_element = soup.find('div', {'class': 'item-not-found-image'})
            # if error_message_element:
            #     return "No"
        except Exception as e:
            print("Error for product ", id)
            return "Error"

        # If no error message is found, assume the page has a product
        return "No"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return "Error"


def checkID(id):
    h = httplib2.Http()
    url = 'https://www.aliexpress.com/item/' + str(id) + '.html'
    resp = h.request(url, 'HEAD')
    return "Yes" if (int(resp[0]['status']) < 400) else "No"


# TO DO: Error handling, type safety, add methods for other actions
class ShopifyAPI:

    def __init__(self):
        self.api = ShopifyAPI.URLs()

    class URLs:
        manager = ShopifyManager()
        # Endpoints
        products = "products.json"
        products_count = "products/count.json"

        def get_products_url(self):
            return self.manager.get_api_url() + self.products

        def get_products_count_url(self):
            return self.manager.get_api_url() + self.products_count

        def get_product_url(self, product_id):
            return self.manager.get_api_url() + "products/" + product_id + ".json"

        def new_product_url(self):
            return self.manager.get_api_url() + self.products

        def update_product_url(self, product_id):
            return self.manager.get_api_url() + "products/" + product_id + ".json"

        def delete_product_url(self):
            return self.manager.get_api_url() + self.products

    # TESTED, WORKS
    def get_product_count(self):
        request = self.api.get_products_count_url()
        # Get result, convert to json, split on "count" key, to get the value
        products_count = requests.get(request).json()["count"]
        return products_count

    # TO BE TESTED
    def get_products_list(
            self,
            ids=None,
            collection_id=None,
            limit=None,
            published_status=None,
            status=None,
            vendor=None
    ):
        url = self.api.get_products_url()
        need_and = False
        if ids is not None:
            symbol = "&" if need_and else "?"
            url += symbol + "ids=" + ids
            need_and = True
        if collection_id is not None:
            symbol = "&" if need_and else "?"
            url += symbol + "collection_id=" + collection_id
            need_and = True
        if limit is not None:
            symbol = "&" if need_and else "?"
            url += symbol + "limit=" + limit
            need_and = True
        if published_status is not None:
            symbol = "&" if need_and else "?"
            url += symbol + "published_status=" + published_status
            need_and = True
        if status is not None:
            symbol = "&" if need_and else "?"
            url += symbol + "status" + status
            need_and = True
        if vendor is not None:
            symbol = "&" if need_and else "?"
            url += symbol + "vendor" + vendor
        # Get result, convert to json, split on "products" key
        products_list = requests.get(url).json()["products"]
        # ["products"]
        # products_list = requests.post(url, json=body).json()
        return products_list

    # TESTED, WORKS
    def get_product_ids(self):
        request = self.api.get_products_url()
        # Get result, convert to json, split on "products" key 
        products_list = requests.get(request).json()["products"]
        ids = []
        for p_id in products_list:
            ids.append(p_id["id"])
        return ids

    def get_product_ids2(self):
        # request = self.api.get_products_url()
        # Get result, convert to json, split on "products" key
        # products_list = requests.get(request).json()["products"]
        products_list = self.get_products_list(limit='250')
        ids = set()
        for product in products_list:
            for variant in product['variants']:
                sku = variant['sku']
                # print(sku)
                ids.add(sku)

            # for variant in product['options']:
            #     ids.add(variant['id'])
        # for p_id in products_list:
        #     ids.append(p_id["id"])
        return list(ids)

    # def get_product_ids2(self):
    #     # request = self.api.get_products_url()
    #     # Get result, convert to json, split on "products" key
    #     # products_list = requests.get(request).json()["products"]
    #     products_list = self.get_products_list(limit='250')
    #     products = set()
    #     for product in products_list:
    #         name = product['title']
    #         for variant in product['options']:
    #             ali_id = variant['id']
    #             ids.add()
    #     # for p_id in products_list:
    #     #     ids.append(p_id["id"])
    #     return list(ids)

    # TESTED, WORKS
    def get_product(self, product_id):
        request = self.api.get_product_url(product_id)
        fetch_product = requests.get(request).json()
        print(fetch_product)
        return fetch_product["product"]

    # Need model new product to test
    def create_product(self, product):
        request = self.api.new_product_url()
        print(product)
        new_product = requests.post(request, data=product)
        return new_product

    # Need to post
    def update_product(self, product_id, variants):
        request = self.api.update_product_url(product_id)
        updated_product = {'product': {'id': product_id, 'variants': variants}}
        print(updated_product)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        # updated_product = requests.put(request, json=updated_product)
        try:
            updated_product = requests.put(request, json=updated_product, headers=headers)
            updated_product.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("Update product: ", product_id, " error: ", err)

        return updated_product

    # Status change works, need to post it up again
    def set_inactive_product(self, product_id):
        product = self.get_product(product_id)
        request = self.api.update_product_url()

        product["status"] = "inactive"

        with open("sample.json", "w") as outfile:
            json.dump(product, outfile)

        updated_product = requests.put(request, product).json()
        return updated_product

    # TESTED, WORKS
    def delete_product(self, product_id):
        request = self.api.get_product_url(product_id)
        deleted_product = requests.delete(request).json()
        return deleted_product

    def create_aliexpress_catalogue(self):
        ids = self.get_product_ids2()
        file_name = 'iDeal-AliExpress-Products-' + str(date.today()) + '.csv'
        heading = [
            'AliExpess ID',
            'AliExpess Link',
            'Exist',
            'URL',
            'Name'
        ]
        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            theWriter = writer(f)
            theWriter.writerow(heading)
            for id in ids:
                row = [
                    id,
                    'https://www.aliexpress.com/item/' + str(id) + '.html'
                ]
                theWriter.writerow(row)


if __name__ == '__main__':
    manager = ShopifyAPI()
    manager.create_aliexpress_catalogue()
    # ids = manager.get_product_ids2()
    # print(is_valid_aliexpress_link(1))
    # for index, id in enumerate(ids):
    #      print(index, " id= ", id, " in aliexpress: ", is_valid_aliexpress_link(id))

    # print("Get products: \n", manager.get_product_ids2())
    # product = manager.get_product('8442271924558')
    # print("Get products: \n", manager.get_products_list(limit='10'))
    # id = '8431637397838'
    # variants = []
    # variant = {
    #     'id': '46796162793806',
    #     'price': 94.99,
    #     'compare_at_price': 163.99
    # }
    # variants.append(variant)
    # manager.update_product(id, variants)
    # print("Product Updated")

    # product["product"]["id"] = '9442271924558'
    # new_product = manager.create_product(product)

    # updated_product = manager.set_inactive_product('8442271924558')

    # print(product)

    # deleted_product = manager.delete_product('8442271924558')
    # product_list = manager.get_products_list()
    # for prod in product_list:
    #     print(prod)
    # product_ids = manager.get_product_count()
    # print(product_ids)
    # print(product)
    # print(dir(product))
    # print(product)
    # print(new_product)
    # print(new_product["status"])
