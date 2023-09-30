"""
 * Author:    Andreas Naoum
 * Created:   30.09.2023
 *
 * (c) Copyright iDeal
"""

import requests
from ShopifyManager import ShopifyManager


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

        def get_product_url(self, product_id):
            return self.manager.get_api_url() + "products/" + product_id + ".json"

        def new_product_url(self):
            return self.manager.get_api_url() + self.products

        def update_product_url(self):
            return self.manager.get_api_url() + self.products

        def delete_product_url(self):
            return self.manager.get_api_url() + self.products

    def get_products_list(self):
        return

    def get_product(self, product_id):
        request = self.api.get_product_url(product_id)
        fetch_product = requests.get(request)
        return fetch_product.json()

    def create_product(self, product):
        return

    def update_product(self, product):
        return

    def set_inactive_product(self, product_id):
        return

    def delete_product(self, product):
        return


if __name__ == '__main__':
    manager = ShopifyAPI()
    print(manager.get_product('8510061379918'))
