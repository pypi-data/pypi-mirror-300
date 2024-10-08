import urllib3

from types import TracebackType
import logging

CLIENT_CREDS_ENV_VARS = {
    "client_id": "OCHRE_CLIENT_ID",
    "client_secret": "OCHRE_CLIENT_SECRET",
    "client_username": "OCHRE_CLIENT_USERNAME",
    "redirect_uri": "OCHRE_REDIRECT_URI",
}


class Retry(urllib3.Retry):
    """
    Class for returning whether the API is rate limited
    """
    def increment(
        self,
        method: str | None = None,
        url: str | None = None,
        response: Exception | None = None,
        error: Exception | None = None,
        _pool: urllib3.connectionpool.ConnectionPool | None = None,
        _stacktrace: TracebackType | None = None,
    ) -> urllib3.Retry:
        if response:
            retry_header = response.headers.get("Retry-After")
            if self.is_retry(method, response.status, bool(retry_header)):
                logging.warning("Your application has reached a rate/request limit. "
                                f"Retry will occur after: {retry_header}")
        return super().increment(method,
                                 url,
                                 response,
                                 error,
                                 _pool,
                                 _stacktrace)
        
def normalize_scope(scope):
    if scope:
        if isinstance(scope, str):
            scopes = scope.split(',')
        elif isinstance(scope, list) or isinstance(scope, tuple):
            scopes = scope
        else:
            raise Exception(
                "Unsupported scope value, please either provide a list of scopes, "
                "or a string of scopes separated by commas."
            )
        return " ".join(sorted(scopes))
    else:
        return None
    
    

def build_params(*args, **kwargs):
    """
    Build a dictionary of parameters, excluding None values.
    
    :param args: Positional arguments (values)
    :param kwargs: Keyword arguments (if you want to specify parameter names)
    :return: Dict of parameters with non-None values
    """
    if kwargs:
        return {k: v for k, v in kwargs.items() if v is not None}
    else:
        return {k: v for k, v in zip(build_params.param_names, args) if v is not None}