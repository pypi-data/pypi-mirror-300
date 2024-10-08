from ochrepy.util import build_params

class Stores:
    def __init__(self, client):
        self.client = client

    def list(self, page=1, limit=10):
        params = build_params(
            page,
            limit
        )
        return self.client._internal_call("GET", "retail/stores", params=params)

    def get(self, store_id):
        return self.client._internal_call("GET", f"retail/stores/{store_id}")

    def create(self, data):
        return self.client._internal_call("POST", "retail/stores", payload=data)

    def update(self, store_id, data):
        return self.client._internal_call("PUT", f"retail/stores/{store_id}", payload=data)

    def delete(self, store_id):
        return self.client._internal_call("DELETE", f"retail/stores/{store_id}")
    