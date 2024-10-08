from ochrepy.util import build_params

class Spaces:
    def __init__(self, client):
        self.client = client

    def list(self, name=None, type=None, owner_id=None, owner_name=None, page=1, limit=10):
        input_params = {
            'view_id': name,
            'type': type,
            'owner_id': owner_id,
            'owner_name': owner_name,
            'page': page,
            'limit': limit
        }
        params = build_params(input_params)
        return self.client._internal_call("GET", "cms/spaces", params=params)

    def get(self, space_id):
        return self.client._internal_call("GET", f"cms/spaces/{space_id}")

    def create(self, data):
        return self.client._internal_call("POST", "cms/spaces", payload=data)

    def update(self, space_id, data):
        return self.client._internal_call("PUT", f"cms/spaces/{space_id}", payload=data)

    def delete(self, space_id):
        return self.client._internal_call("DELETE", f"cms/spaces/{space_id}")

    def navigation_items(self, space_id, page=1, limit=10, group_id=None):
        params = build_params(
            page,
            limit,
            group_id
        )
        return self.client._internal_call("GET", f"cms/spaces/{space_id}/navigation-items", params=params)

    def views(self, space_id, type=None, reference_type=None, reference_id=None, slug=None, title=None, page=1, limit=10):
        params = build_params(
            type,
            reference_type,
            reference_id,
            slug,
            title,
            page,
            limit
        )
        return self.client._internal_call("GET", f"cms/spaces/{space_id}/views", params=params)