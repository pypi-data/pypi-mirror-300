from ochrepy.util import build_params

class Tracks:
    def __init__(self, client):
        self.client = client

    def list(self, page=1, limit=10, **kwargs):
        """
        List tracks with various filter options.

        :param page: Page number for pagination (default: 1)
        :param limit: Number of items per page (default: 10)
        :param kwargs: Additional filter parameters. Can include:
                    release_id, artist_id
        :return: List of tracks matching the criteria
        """
        input_params = {
            'page': page,
            'limit': limit,
            **kwargs
        }
        params = build_params(**input_params)
        return self.client._internal_call("GET", "music/tracks", params=params)

    def get(self, track_id):
        return self.client._internal_call("GET", f"music/tracks/{track_id}")

    def create(self, data):
        return self.client._internal_call("POST", "music/tracks", payload=data)

    def update(self, track_id, data):
        return self.client._internal_call("PUT", f"music/tracks/{track_id}", payload=data)

    def delete(self, track_id):
        return self.client._internal_call("DELETE", f"music/tracks/{track_id}")
    
    def media_items(self, track_id, page=1, limit=10, **kwargs):
        #
        """
        List tracks with various filter options.

        :param page: Page number for pagination (default: 1)
        :param limit: Number of items per page (default: 10)
        :param kwargs: Additional filter parameters. Can include:
                    type, format, service, catalog_id, 
                    from, to, include_references
        :return: List of tracks matching the criteria
        """
        input_params = {
            'track_id': track_id,
            'page': page,
            'limit': limit,
            **kwargs
        }
        params = build_params(**input_params)
        return self.client._internal_call("GET", f"music/tracks/{track_id}/media-items", params=params)
    
    
    
    


    