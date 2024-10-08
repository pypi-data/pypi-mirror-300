import warnings
import logging
import time
import os
import base64

import requests

from .cache_handler import CacheFileHandler, CacheHandler
from .util import CLIENT_CREDS_ENV_VARS, normalize_scope

logger = logging.getLogger(__name__)


class OchreAuthError(Exception):
    
    def __init__(self, message, error=None, error_description=None, *args, **kwargs):
        self.error = error
        self.error_description = error_description
        self.__dict__.update(kwargs)
        super().__init__(message, *args, **kwargs)
        


def _make_authorization_headers(client_id, client_secret):
    auth_header = base64.b64encode(
        str(client_id + ":" + client_secret).encode("ascii")
    )
    return {"Authorization": f"Basic {auth_header.decode('ascii')}"}


def _ensure_value(value, env_key):
    env_val = CLIENT_CREDS_ENV_VARS[env_key]
    _val = value or os.getenv(env_val)
    if _val is None:
        msg = f"No {env_key}. Pass it or set a {env_val} environment variable."
        raise OchreAuthError(msg)
    return _val


class OchreAuthBase:
    def __init__(self,
                 requests_session
                 ):
        if isinstance(requests_session, requests.Session):
            self._session = requests_session
        else:
            if requests_session: # Build a new session
                self._session = requests.Session()
            else: # Use the requests api module as a "session"
                from requests import api
                self._session = api
                
    def _normalize_scope(self, scope):
        return normalize_scope(scope)
    
    @property
    def client_id(self):
        return self._client_id
    
    @client_id.setter
    def client_id(self, val):
        self._client_id = _ensure_value(val, "client_id")
        
    @property
    def client_secret(self):
        return self._client_secret
    
    @client_secret.setter
    def client_secret(self, val):
        self._client_secret = _ensure_value(val, "client_secret")
        
    @property
    def redirect_url(self):
        return self._redirect_url
    
    @redirect_url.setter
    def redirect_url(self, val):
        self._redirect_url = _ensure_value(val, "redirect_url")
        
    @staticmethod
    def _get_user_inut(prompt):
        try:
            return raw_input(prompt) # type: ignore
        except NameError:
            return input(prompt)
        
    @staticmethod
    def is_token_expired(token_info):
        now = int(time.time())
        return token_info["expires_at"] - now < 60
    
    @staticmethod
    def _is_scope_subset(needle_scope, haystack_scope):
        needle_scope = set(needle_scope.split()) if needle_scope else set()
        haystack_scope = (
            set(haystack_scope.split()) if haystack_scope else set()
        )
        return needle_scope <= haystack_scope
    
    def _handle_auth_error(self, http_error):
        response = http_error.response
        try:
            error_payload = response.json()
            error = error_payload.get("error")
            error_description = error_payload.get("error_description")
        except ValueError:
            error = response.text or None
            error_description = None
        
        raise OchreAuthError(
            f'error: {error}, error_description: {error_description}',
            error,
            error_description
        )
        
    def __del__(self):
        if isinstance(self._session, requests.Session):
            self._session.close()


class OchreClientCredentials(OchreAuthBase):
    AUTH_TOKEN_URL = "https://auth.ochre.io/oauth2/token"
    
    def __init__(
        self,
        client_id=None,
        client_secret=None,
        proxies=None,
        requests_session=True,
        requests_timeout=None,
        cache_handler=None
    ):
        
        super().__init__(requests_session)
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.proxies = proxies
        self.requests_timeout = requests_timeout
        if cache_handler:
            assert issubclass(cache_handler.__class__, CacheHandler), \
                "cache_handler must be a subclass of CacheHandler: " + str(type(cache_handler)) \
                + " != " + str(CacheHandler)
            self.cache_handler = cache_handler
        else:
            self.cache_handler = CacheFileHandler()
            
    def get_access_token(self, as_dict=True, check_cache=True):
        if as_dict:
            warnings.warn(
                "You're using 'as_dict = True'."
                "get_access_token will return the token string directly in future "
                "versions. Please adjust your code accordingly, or use "
                "get_cached_token instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            
        if check_cache:
            token_info = self.cache_handler.get_cached_token()
            if token_info and not self.is_token_expired(token_info):
                return token_info if as_dict else token_info["access_token"]
            
        token_info = self._request_access_token()
        token_info = self._add_custom_values_to_token_info(token_info)
        self.cache_handler.save_token_to_cache(token_info)
        return token_info if as_dict else token_info["access_token"]
        
    def _request_access_token(self):
        payload = {
            "grant_type": "client_credentials", 
            "client_id": self.client_id,
            "client_secret": self.client_secret
            }
        
        logger.debug(
            "sending POST request to %s with Body: %r",
            self.AUTH_TOKEN_URL, payload
        )
        
        try:
            response = self._session.post(
                self.AUTH_TOKEN_URL,
                data=payload,
                verify=True,
                proxies=self.proxies,
                timeout=self.requests_timeout,
            )
            response.raise_for_status()
            token_info = response.json()
            return token_info
        except requests.exceptions.HTTPError as http_error:
            self._handle_auth_error(http_error)
        
    def _add_custom_values_to_token_info(self, token_info):
        token_info["expires_at"] = int(time.time()) + token_info["expires_in"]
        return token_info
            