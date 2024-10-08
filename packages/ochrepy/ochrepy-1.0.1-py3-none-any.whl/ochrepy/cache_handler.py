import os
import json
import errno
import logging

from .util import CLIENT_CREDS_ENV_VARS

logger = logging.getLogger(__name__)

class CacheHandler():
    pass

class CacheFileHandler(CacheHandler):
    def __init__(self,
                 cache_path=None,
                 username=None,
                 encoder_cls=None):
        
        self.encoder_cls = encoder_cls
        if cache_path:
            self.cache_path = cache_path
        else:
            cache_path = ".cache"
            username = (username or os.getenv(CLIENT_CREDS_ENV_VARS["client_username"]))
            if username:
                cache_path += "-" + str(username)
            self.cache_path = cache_path
            
        
    def get_cached_token(self):
        token_info = None
        
        try: 
            f = open(self.cache_path)
            token_info_string = f.read()
            f.close()
            token_info = json.loads(token_info_string)
            
        except OSError as error:
            if error.errno == errno.ENOENT:
                logger.debug("cache does not exist at: %s", self.cache_path)
            else:
                logger.warning("Couldn't read cache at: %s", self.cache_path)
                
        return token_info
    
    def save_token_to_cache(self, token_info):
        try:
            f = open(self.cache_path, "w")
            f.write(json.dumps(token_info, cls=self.encoder_cls))
            f.close()
        except OSError:
            logger.warning('Couldn\'t write token to cache at: %s',
                           self.cache_path)