from ochrepy.util import build_params

class Views:
    def __init__(self, client):
        self.client = client

    def list(self, space_id=None, type=None, reference_type=None, reference_id=None, slug=None, title=None, page=1, limit=10):
        params = build_params(
            space_id,
            type,
            reference_type,
            reference_id,
            slug,
            title,
            page,
            limit
        )
        return self.client._internal_call("GET", "cms/views", params=params)

    def get(self, view_id):
        return self.client._internal_call("GET", f"cms/views/{view_id}")

    def create(self, data):
        return self.client._internal_call("POST", "cms/views", payload=data)

    def update(self, view_id, data):
        return self.client._internal_call("PUT", f"cms/views/{view_id}", payload=data)

    def delete(self, view_id):
        return self.client._internal_call("DELETE", f"cms/views/{view_id}")

    def modules(self, view_id, title=None, type=None, page=1, limit=10):
        params = build_params(
            title,
            type,
            page,
            limit
        )
        return self.client._internal_call("GET", f"cms/views/{view_id}/modules", params=params)

    