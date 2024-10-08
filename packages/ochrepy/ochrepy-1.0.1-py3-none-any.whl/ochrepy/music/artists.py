from ochrepy.util import build_params

class Artists:
    def __init__(self, client):
        self.client = client

    def list(self, name=None, active=None, catalog_id=None, page=1, limit=10):
        params = build_params(name, active, catalog_id, page, limit)
        return self.client._internal_call("GET", "music/artists", params=params)

    def get(self, artist_id):
        return self.client._internal_call("GET", f"music/artists/{artist_id}")

    def create(self, data):
        return self.client._internal_call("POST", "music/artists", payload=data)

    def update(self, artist_id, data):
        return self.client._internal_call("PUT", f"music/artists/{artist_id}", payload=data)

    def delete(self, artist_id):
        return self.client._internal_call("DELETE", f"music/artists/{artist_id}")
    
    def releases(self, artist_id, page=1, limit=10, **kwargs):
        params = build_params(page, limit, **kwargs)
        return self.client._internal_call("GET", f"music/artists/{artist_id}/releases", params=params)
    
    def tracks(self, artist_id, release_id=None, page=1, limit=10):
        params = build_params(release_id, page, limit)
        return self.client._internal_call("GET", f"music/artist/{artist_id}/tracks", params=params)
    
    
    
    


    