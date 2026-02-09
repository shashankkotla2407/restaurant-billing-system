class Order:
    def __init__(self):
        self.cart = {}

    def add_item(self, item_id, name, price, qty=1):
        if item_id in self.cart:
            self.cart[item_id]["qty"] += qty
        else:
            self.cart[item_id] = {"name": name, "price": price, "qty": qty}

    def is_empty(self):
        return len(self.cart) == 0

    def get_cart_items(self):
        items = []
        for item_id, item in self.cart.items():
            line_total = item["price"] * item["qty"]
            items.append({
                "item_id": item_id,
                "item_name": item["name"],
                "quantity": item["qty"],
                "price": item["price"],
                "total": round(line_total, 2)
            })
        return items
    
    def set_quantity(self, item_id, qty):
        if item_id in self.cart:
            if qty <= 0:
                del self.cart[item_id]
            else:
                self.cart[item_id]["qty"] = qty

    def get_subtotal(self):
        subtotal = 0
        for item in self.cart.values():
            subtotal += item["price"] * item["qty"]
        return round(subtotal, 2)

    def clear_cart(self):
        self.cart = {}
    
    def remove_item(self, item_id):
        if item_id in self.cart:
            del self.cart[item_id]
