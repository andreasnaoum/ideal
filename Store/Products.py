"""
 * Author:    Andreas Naoum
 * Created:   30.09.2023
 *
 * (c) Copyright iDeal
"""
from enum import Enum


class Collection(Enum):
    IPHONE = "iPhone"
    IPAD = "iPad"
    MAC = "Mac"
    AIRPODS = "AirPods"
    WATCH = "Watch"
    SMART_HOME = "Home"
    HEALTH_FITNESS = "Health"


class Tags(Enum):
    IPHONE_CASE = "iphone-case"
    IPHONE_PROTECTOR = "iphone-protector"
    IPHONE_CHARGER = "iphone-charger"
    IPHONE_MOUNT = "iphone-mount"
    IPHONE_STAND = "iphone-stand"
    IPHONE_OTHER = "iphone-other"
    IPAD_CASE = "ipad-case"
    IPAD_CHARGER = "ipad-charger"
    IPAD_CABLE = "ipad-cables"
    IPAD_KEYBOARD = "ipad-keyboard"
    IPAD_PENCIL = "ipad-pencil"
    IPAD_HUB = "ipad-hub"
    IPAD_OTHER = "ipad-other"
    MAC_CASE = "mac-case"
    MAC_CHARGER = "mac-case"
    MAC_CABLE = "mac-cables"
    MAC_KEYBOARD = "mac-keyboard"
    MAC_STAND = "mac-stand"
    MAC_STORAGE = "mac-storage"
    MAC_PROTECTOR = "mac-protector"
    MAC_OTHER = "mac-other"
    AIRPODS = "airpods"
    WATCH_BAND = "watch-band"
    WATCH_CASE = "watch-case"
    WATCH_PROTECTOR = "watch-protector"
    WATCH_CHARGER = "watch-charger"
    WATCH_OTHER = "watch-other"
    SMART_HOME_SENSOR = "home-sensor"
    SMART_HOME_HUMIDIFIER = "home-humidifier"
    SMART_HOME_LIGHT = "home-light"
    SMART_HOME_THERMOSTAT = "home-thermostat"
    SMART_HOME_PLUGS = "home-plugs"
    SMART_HOME_SWITCH = "home-switch"
    SMART_HOME_CAMERA = "home-camera"
    SMART_HOME_KITCHEN = "home-kitchen"


class Supplier(Enum):
    ALIEXPRESS = "aliexpress"
    GEEKBUYING = "geekbuying"


class Product:
    "Represenation of data samles"

    def __init__(self, code, collection, deal, tags):

        if not isinstance(collection, Collection):
            raise ValueError("Invalid collection")

        if not all(isinstance(tag, Tags) for tag in tags):
            raise ValueError("Invalid tags")

        self.url = code
        self.collection = collection
        self.deal = deal
        self.tags = tags


    def is_valid_product(self):
        # Check if collection is valid
        if not isinstance(self.collection, Collection):
            return False

        # Check if tags are valid
        if not all(isinstance(tag, Tags) for tag in self.tags):
            return False

        return True

    def get_url(self):
        return 'https://www.aliexpress.com/item/' + self.code + '.html'

    # Function to calculate the final price
    def calculate_final_price(self, base_price, profit_margin, discount):
        # Calculate the initial price with profit margin
        initial_price = base_price * profit_margin

        # Apply random discount within the given range
        final_price = initial_price * (1 - discount)

        # Apply first purchase discount
        # final_price = discounted_price

        return initial_price, final_price