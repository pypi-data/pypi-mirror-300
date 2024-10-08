from ochrepy.util import build_params

class MediaItems:
    def __init__(self, client):
        self.client = client

    def list(self, page=1, limit=10, **kwargs):
        """
        List media items with various filter options.

        :param page: Page number for pagination (default: 1)
        :param limit: Number of items per page (default: 10)
        :param kwargs: Additional filter parameters. Can include:
                    reference_type, reference_id, type, format,
                    service, catalog_id, from, to, include_references
        :return: List of media items matching the criteria
        """
        params = build_params(page, limit, **kwargs)
        return self.client._internal_call("GET", "music/media-items", params=params)

    def get(self, media_item_id):
        return self.client._internal_call("GET", f"music/media-items/{media_item_id}")

    def create(self, data):
        return self.client._internal_call("POST", "music/media-items", payload=data)

    def update(self, media_item_id, data):
        return self.client._internal_call("PUT", f"music/media-items/{media_item_id}", payload=data)

    def delete(self, media_item_id):
        return self.client._internal_call("DELETE", f"music/media-items/{media_item_id}")
    
    
    
    


    