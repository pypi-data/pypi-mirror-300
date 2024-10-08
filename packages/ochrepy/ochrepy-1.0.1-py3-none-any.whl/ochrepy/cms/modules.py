from ochrepy.util import build_params

class Modules:
    def __init__(self, client):
        self.client = client

    def list(self, view_id=None, title=None, type=None, page=1, limit=10):
        input_params = {
            'view_id': view_id,
            'title': title,
            'type': type,
            'page': page,
            'limit': limit
        }
        params = build_params(input_params)
        return self.client._internal_call("GET", "cms/modules", params=params)

    def get(self, module_id):
        return self.client._internal_call("GET", f"cms/modules/{module_id}")

    def create(self, data):
        return self.client._internal_call("POST", "cms/modules", payload=data)

    def update(self, module_id, data):
        return self.client._internal_call("PUT", f"cms/modules/{module_id}", payload=data)

    def delete(self, module_id):
        return self.client._internal_call("DELETE", f"cms/modules/{module_id}")

    def content_items(self, module_id, page=1, limit=10):
        input_params = {
            'page': page,
            'limit': limit
        }
        params = build_params(input_params)
        return self.client._internal_call("GET", f"cms/modules/{module_id}/content-items", params=params)

    