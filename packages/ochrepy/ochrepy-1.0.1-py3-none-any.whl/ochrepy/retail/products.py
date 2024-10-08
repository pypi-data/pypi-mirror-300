from ochrepy.util import build_params

class Products:
    def __init__(self, client):
        self.client = client

    def list(self, page=1, limit=10, **kwargs):
        """
        List products with various filter options.

        :param page: Page number for pagination (default: 1)
        :param limit: Number of items per page (default: 10)
        :param kwargs: Additional filter parameters. Can include:
                    store_id, catalog_id, group_id, variant_group_id, title, type,
                    reference_type, reference_id, from, to, format, universe,
                    distribution, variant, allow_preorder
        :return: List of products matching the criteria
        """
        all_params = {
            'page': page,
            'limit': limit,
            **kwargs
        }
        params = build_params(**all_params)
        return self.client._internal_call("GET", "retail/products", params=params)

    def get(self, product_id):
        return self.client._internal_call("GET", f"retail/products/{product_id}")

    def create(self, data):
        return self.client._internal_call("POST", "retail/products", payload=data)

    def update(self, product_id, data):
        return self.client._internal_call("PUT", f"retail/products/{product_id}", payload=data)

    def delete(self, product_id):
        return self.client._internal_call("DELETE", f"retail/products/{product_id}")
    
    def availability(self, product_id):
        return self.client._internal_call("GET", f"retail/products/{product_id}/availability")
    
    def bundle_items(self, product_id, page=1, limit=10):
        params = build_params(page, limit)
        return self.client._internal_call("GET", f"retail/products/{product_id}/bundle-items", params=params)
    


    