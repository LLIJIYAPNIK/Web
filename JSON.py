import json


class Products:
    def __init__(self):
        self.js_file = json.load(open("products.json", "r", encoding='utf-8'))

    # get Category
    def get_category_ids(self, _type=None):
        if isinstance(_type, set):
            return set(self.js_file["category"])
        return self.js_file["category"]

    def get_all_category(self):
        return self.js_file["all"]

    def get_category(self, _id):
        _id = str(_id)
        if _id in self.get_category_ids(_type=set):
            return self.js_file["all"][_id]
        else:
            return {
                "methods": "get_category",
                "error": "id"
            }

    # get Product
    def get_products_id(self, _type=None):
        if isinstance(_type, set):
            return set(self.js_file["products_id"])
        return self.js_file["products_id"]

    def get_all_products(self):
        return self.js_file["products"]

    def get_products(self, _id):
        _id = str(_id)
        if _id in self.get_products_id(_type=set):
            return self.js_file["products"][_id]
        else:
            return {
                "methods": "get_products",
                "error": "id"
            }

    def get_card_compressed(self):
        return set(self.js_file["calories"])