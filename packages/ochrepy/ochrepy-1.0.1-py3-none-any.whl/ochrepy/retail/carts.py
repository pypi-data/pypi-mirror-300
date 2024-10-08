from ochrepy.util import build_params

class Carts:
    def __init__(self, client):
        self.client = client

    def get(self, cart_id):
        return self.client._internal_call("GET", f"retail/carts/{cart_id}")

    def create(self, data):
        return self.client._internal_call("POST", "retail/carts", payload=data)

    def update(self, cart_id, data):
        return self.client._internal_call("PUT", f"retail/carts/{cart_id}", payload=data)

    def delete(self, cart_id):
        return self.client._internal_call("DELETE", f"retail/carts/{cart_id}")
    
    def items(self, cart_id, page=1, limit=10):
        params = build_params(page, limit)
        return self.client._internal_call("GET", f"retail/carts/{cart_id}/items", params=params)
    
    def add_items(self, cart_id, payload):
        return self.client._internal_call("POST", f"retail/carts/{cart_id}/items", payload=payload)
    
    def get_item(self, cart_id, item_id):
        return self.client._internal_call("GET", f"retail/carts/{cart_id}/items/{item_id}")
    
    def update_item(self, cart_id, item_id, payload):
        return self.client._internal_call("PUT", f"retail/carts/{cart_id}/items/{item_id}", payload=payload)
    
    def delete_item(self, cart_id, item_id):
        return self.client._internal_call("DELETE", f"retail/carts/{cart_id}/items/{item_id}")
    
    def vouchers(self, cart_id, page=1, limit=10):
        params = build_params(page, limit)
        return self.client._internal_call("GET", f"retail/carts/{cart_id}/vouchers", params=params)
    