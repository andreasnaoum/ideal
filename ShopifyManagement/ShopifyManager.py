"""
 * Author:    Andreas Naoum
 * Created:   30.09.2023
 *
 * (c) Copyright iDeal
"""


class ShopifyManager:
    ADMIN_API_KEY = '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'
    API_KEY = 'e5bcdda95a0354ed2d4e351585bbf274'
    API_SECRET = '7166687afd9d38dd9dbb8311eb36cd08'

    def get_api_url(self):
        return 'https://' + self.API_KEY + ":" + self.ADMIN_API_KEY + '@ideal-2676.myshopify.com/admin/api/2023-07/'
