import uuid


class Product:
    def __init__(self, owner_id, name, category, price, quantity, date_added):
        self.product_id = str(uuid.uuid4())
        self.owner_id = owner_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.date_added = date_added
