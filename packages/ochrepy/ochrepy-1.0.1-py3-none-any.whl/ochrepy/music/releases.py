from ochrepy.util import build_params

class Releases:
    def __init__(self, client):
        self.client = client

    def list(self, page=1, limit=10, **kwargs):
        """
        List releases with various filter options.

        :param page: Page number for pagination (default: 1)
        :param limit: Number of items per page (default: 10)
        :param kwargs: Additional filter parameters. Can include:
                    title, artist_id, artist_name, label_id,
                    catalog_id, from, to
        :return: List of releases matching the criteria
        """
        params = build_params(page, limit, **kwargs)
        return self.client._internal_call("GET", "music/releases", params=params)

    def get(self, release_id):
        return self.client._internal_call("GET", f"music/releases/{release_id}")

    def create(self, data):
        return self.client._internal_call("POST", "music/releases", payload=data)

    def update(self, release_id, data):
        return self.client._internal_call("PUT", f"music/releases/{release_id}", payload=data)

    def delete(self, release_id):
        return self.client._internal_call("DELETE", f"music/releases/{release_id}")
    
    def tracks(self, release_id, artist_id=None, page=1, limit=10):
        params = build_params(artist_id, page, limit)
        return self.client._internal_call("GET", f"music/releases/{release_id}/tracks", params=params)
    
    
    
    


    