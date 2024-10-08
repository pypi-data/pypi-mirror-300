from ochrepy.util import build_params

class OrderItems:
    def __init__(self, client):
        self.client = client
        
    def list(self, page=1, limit=10, **kwargs):
        """
        List order items with various filter options.

        :param page: Page number for pagination (default: 1)
        :param limit: Number of items per page (default: 10)
        :param kwargs: Additional filter parameters. Can include:
                    store_ids, user_ids, order_id, order_number, 
                    created_from, created_to, total_min, total_max,
                    quantity_min, quantity_max
        :return: List of order items matching the criteria
        """
        all_params = {
            'page': page,
            'limit': limit,
            **kwargs
        }
        params = build_params(**all_params)
        return self.client._internal_call("GET", "retail/order-items", params=params)

    def get(self, order_item_id):
        return self.client._internal_call("GET", f"retail/order-items/{order_item_id}")

    def create(self, data):
        return self.client._internal_call("POST", "retail/order-items", payload=data)

    def update(self, order_item_id, data):
        return self.client._internal_call("PUT", f"retail/orders/{order_item_id}", payload=data)

    def delete(self, order_item_id):
        return self.client._internal_call("DELETE", f"retail/orders/{order_item_id}")
    
    