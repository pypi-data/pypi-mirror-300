from ochrepy.util import build_params

class Labels:
    def __init__(self, client):
        self.client = client

    def list(self, page=1, limit=10):
        params = build_params(page, limit)
        return self.client._internal_call("GET", "music/labels", params=params)

    def get(self, label_id):
        return self.client._internal_call("GET", f"music/labels/{label_id}")

    def create(self, data):
        return self.client._internal_call("POST", "music/labels", payload=data)

    def update(self, label_id, data):
        return self.client._internal_call("PUT", f"music/labels/{label_id}", payload=data)

    def delete(self, label_id):
        return self.client._internal_call("DELETE", f"music/labels/{label_id}")
    


    