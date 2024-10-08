""" A simple and thin Python library for the Ochre Web API """

__all__ = ["Ochre", "OchreException"]


import logging
import json

import requests
import requests.adapters

from ochrepy.exceptions import OchreException
from ochrepy.cms import Spaces, Views, Modules
from ochrepy.retail import Stores, Products, Carts, Orders, OrderItems
from ochrepy.music import Artists, Labels, MediaItems, Releases, Tracks

from .util import Retry


logger = logging.getLogger(__name__)

class OchreAPIClient:
    """"
    
    
    """
    max_retries = 3
    default_retry_codes = (429, 500, 502, 503, 504)
    
    def __init__(
        self,
        auth=None,
        requests_session=True,
        client_credentials_manager=None,
        auth_manager=None,
        proxies=None,
        requests_timeout=5,
        status_forcelist=None,
        retries=max_retries,
        status_retries=max_retries,
        backoff_factor=0.3,
        language=None,
    ):
        
        
        self.prefix = "https://api.ochre.io/v1/"
        self._auth = auth
        self.client_credentials_manager = client_credentials_manager
        self.auth_manager = auth_manager
        self.proxies = proxies
        self.requests_timeout = requests_timeout
        self.status_forcelist = status_forcelist or self.default_retry_codes
        self.backoff_factor = backoff_factor
        self.retries = retries
        self.status_retries = status_retries
        self.language = language
        
        if isinstance(requests_session, requests.Session):
            self._session = requests_session
        else:
            if requests_session: # Build a new session.
                self._build_session()
            else: # Use the Requests API module as a "session".
                self._session = requests.api
                
        
    def set_auth(self, auth):
        self._auth = auth
        
    @property
    def auth_manager(self):
        return self._auth_manager
    
    @auth_manager.setter
    def auth_manager(self, auth_manager):
        if auth_manager is not None:
            self._auth_manager = auth_manager
        else: 
            self._auth_manager = (
                self.client_credentials_manager
            )
            
            
    def __del__(self):
        """Close the connection pool"""
        try:
            if isinstance(self._session, requests.Session):
                self._session.close()
        except AttributeError:
            pass
        
        
    def _build_session(self):
        self._session = requests.Session()
        retry = Retry(
            total=self.retries,
            connect=None,
            read=False,
            allowed_methods=frozenset(['GET', 'POST', 'PUT', 'DELETE']),
            status=self.status_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist)
        
        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
        self._session.mount('http://', adapter)
        self._session.mount('https://', adapter)
        
    def _auth_headers(self):
        if self._auth:
            return {"Authorization": f"Bearer {self._auth}"}
        if not self.auth_manager:
            return {}
        try: 
            token = self.auth_manager.get_access_token(as_dict=False)
        except TypeError:
            token = self.auth_manager.get_access_token()
        return {"Authorization": f"Bearer {token}"}
    
    def _internal_call(self, method, url, payload=None, params=None):
        args = dict(params=params)
        if not url.startswith("http"):
            url = self.prefix + url
        headers = self._auth_headers()
        
        if "content_type" in args["params"]:
            headers["Content-Type"] = args["params"]["content_type"]
            del args["params"]["content_type"]
            if payload:
                args["data"] = payload
        else:
            headers["Content-Type"] = "application/json"
            if payload:
                args["data"] = json.dumps(payload)

        if self.language is not None:
            headers["Accept-Language"] = self.language
            
        logger.debug("Sending %s to %s with Params: %s Headers: %s and Body: %r ",
                        method, url, args.get("params"), headers, args.get("data"))
        
        try:
            response = self._session.request(
                method, url, headers=headers, proxies=self.proxies,
                timeout=self.requests_timeout, **args
            )

            response.raise_for_status()
            results = response.json()
        except requests.exceptions.HTTPError as http_error:
            response = http_error.response
            try:
                json_response = response.json()
                error = json_response.get("error", {})
                if isinstance(error, str):
                    msg = error
                    reason = None
                else:
                    msg = error.get("message")
                    reason = error.get("reason")
            except ValueError:
                msg = response.text or None
                reason = None
            
            logger.error(
                'HTTP Error for %s to %s with Params: %s returned %s due to %s',
                method, url, args.get("params"), response.status_code, msg
            )
            
            raise OchreException(
                response.status_code,
                -1,
                f"{response.url}:\n {msg}",
                reason=reason,
                headers=response.headers
            )
        except requests.exceptions.RetryError as retry_error:
            request = retry_error.request
            logger.error('Max Retries reached')
            try:
                reason = retry_error.args[0].reason
            except (IndexError, AttributeError):
                reason = None
            raise OchreException(
                429,
                -1,
                f"{request.path_url}:\n Max Retries",
                reason=reason
            )
        except ValueError:
            results = None
        
        
        logger.debug('RESULTS: %s', results)
        return results
            
        
class Ochre:
    """
        Creates a Ochre API client.

        :param auth: An access token
        :param requests_session:
            A Requests session object or a truthy value to create one.
            A falsy value disables sessions.
            It should generally be a good idea to keep sessions enabled
            for performance reasons (connection pooling).
        :param client_credentials_manager:
            OchreClientCredentials object
        :param auth_manager:
            OchreClientCredentials
        :param proxies:
            Definition of proxies (optional).
            See Requests doc https://2.python-requests.org/en/master/user/advanced/#proxies
        :param requests_timeout:
            Tell Requests to stop waiting for a response after a given
            number of seconds
        :param status_forcelist:
            Tell requests what type of status codes retries should occur on
        :param retries:
            Total number of retries to allow
        :param status_retries:
            Number of times to retry on bad status codes
        :param backoff_factor:
            A backoff factor to apply between attempts after the second try
            See urllib3 https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html
        :param language:
            The language parameter advertises what language the user prefers to see.
            See ISO-639-1 language code: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
        """
    def __init__(self, auth=None, requests_session=True, client_credentials_manager=None, 
                 auth_manager=None, proxies=None, requests_timeout=5, status_forcelist=None, 
                 retries=OchreAPIClient.max_retries, backoff_factor=0.3, language=None):
        self.client = OchreAPIClient(
            auth=auth,
            requests_session=requests_session,
            client_credentials_manager=client_credentials_manager,
            auth_manager=auth_manager,
            proxies=proxies,
            requests_timeout=requests_timeout,
            status_forcelist=status_forcelist,
            retries=retries,
            backoff_factor=backoff_factor,
            language=language
        )
            
        # CMS
        self.cms_spaces = Spaces(self.client)
        self.cms_views = Views(self.client)
        self.cms_modules = Modules(self.client)
        
        # Retail
        self.retail_stores = Stores(self.client)
        self.retail_products = Products(self.client)
        self.retail_carts = Carts(self.client)
        self.retail_orders = Orders(self.client)
        self.retail_order_items = OrderItems(self.client)
        
        # Music
        self.music_artists = Artists(self.client)
        self.music_labels = Labels(self.client)
        self.music_media_items = MediaItems(self.client)
        self.music_releases = Releases(self.client)
        self.music_tracks = Tracks(self.client)