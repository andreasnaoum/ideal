"""
 * Author:    Andreas Naoum
 * Created:   30.09.2023
 *
 * (c) Copyright iDeal
"""

import requests
import json
from ShopifyManager import ShopifyManager

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

        def update_product_url(self):
            return self.manager.get_api_url() + self.products

        def delete_product_url(self):
            return self.manager.get_api_url() + self.products
    
    # TESTED, WORKS
    def get_product_count(self):
        request = self.api.get_products_count_url()

        # Get result, convert to json, split on "count" key, to get the value
        products_count = requests.get(request).json()["count"]
        return products_count

    # TESTED, WORKS
    def get_products_list(self):
        request = self.api.get_products_url()
        
        # Get result, convert to json, split on "products" key 
        products_list = requests.get(request).json()["products"]
        return products_list
    
    # TESTED, WORKS
    def get_product_ids(self):
        request = self.api.get_products_url()
        # Get result, convert to json, split on "products" key 
        products_list = requests.get(request).json()["products"]
        ids=[]
        for p_id in products_list:
            ids.append(p_id["id"])
        return ids

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
    def update_product(self, product):
        request = self.api.update_product_url()
        updated_product = requests.put(request, product.json()).json()
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


if __name__ == '__main__':
    manager = ShopifyAPI()
    product = manager.get_product('8442271924558')

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
    