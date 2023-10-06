from ShopifyManagement.ShopifyAPI import ShopifyAPI
from currency_converter import CurrencyConverter


def convertSEKtoEUR(converter, price):
    print("Converter: ", price)
    new_price = converter.convert(price, 'SEK', 'EUR')
    return round(new_price) - 0.01


if __name__ == '__main__':
    manager = ShopifyAPI()
    converter = CurrencyConverter()
    products = manager.get_products_list(limit='250')
    # print(products[4])
    # x = 5
    for product in products:
        variants = product['variants']
        updated_variants = []
        for variant in variants:
            price = variant['price']
            converter_price = convertSEKtoEUR(converter, price)
            try:
                compared_price = float(variant['compare_at_price'])
                converter_compared_price = convertSEKtoEUR(converter, compared_price)
            except:
                compared_price = 0
                converter_compared_price = 0
            print("Product: ", product['title'], " price: ", price, compared_price, converter_price,
                  converter_compared_price)
            if converter_compared_price > 0:
                updated_variant = {
                    'id': variant['id'],
                    'price': converter_price,
                    'compare_at_price': converter_compared_price
                }
            else:
                updated_variant = {
                    'id': variant['id'],
                    'price': converter_price
                }
            updated_variants.append(updated_variant)
        manager.update_product(str(product['id']), updated_variants)
        # if x == 5:
        #     print("Updated Product 5: ", str(product['id']), str(product['title']))
        #     manager.update_product(str(product['id']), updated_variants)
        # x += 1