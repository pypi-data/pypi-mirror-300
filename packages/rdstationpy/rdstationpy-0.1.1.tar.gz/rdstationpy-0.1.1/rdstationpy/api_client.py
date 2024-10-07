from urllib.parse import urlencode

import requests
from requests.adapters import HTTPAdapter
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    stop_never,
    wait_exponential,
)

from rdstationpy.exceptions import RDStationException
from rdstationpy.utils.config import get_default_config


class ApiClient:
    def __init__(self, api_key, url, config=None):
        assert api_key is not None, "API Key must be set"
        self.api_key = api_key
        print(url)
        self.url = url
        print(self.url)

        if config is None:
            self.config = get_default_config()
        else:
            assert isinstance(config, dict)
            self.config = config

        self._create_session()
        self.max_attempts = self.config.get("max_attempts", 10)

    def _create_session(self):
        self._session = requests.Session()
        adapter = HTTPAdapter()
        self._session.mount("https://", adapter)

    def _is_retryable_exception(self, exception):
        print(exception)
        return isinstance(
            exception, RDStationException
        ) and exception.http_code in self.config.get("default_retry_codes")

    def _get_retry_decorator(self):
        max_attempts = self.config.get("max_attempts", 10)

        return retry(
            stop=stop_after_attempt(max_attempts)
            if max_attempts is not None
            else stop_never,
            wait=wait_exponential(multiplier=1, min=1, max=60),
            retry=retry_if_exception(self._is_retryable_exception),
        )

    def make_request(self, method, resource, data={}, **kwargs):
        kwargs.setdefault("token", self.api_key)
        print(kwargs)
        query_string = urlencode(kwargs)

        url = f"{self.url}{resource}?{query_string}"

        headers = {"accept": "application/json", "content-type": "application/json"}

        if "page" in kwargs.keys():
            page = kwargs["page"]
        else:
            page = 1

        @self._get_retry_decorator()
        def _call_request(method, url, data, headers):
            try:
                response = self._session.request(
                    method, url, json=data, headers=headers
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as http_error:
                raise RDStationException(
                    http_error.response.status_code, http_error.response.json()
                )
            # Is treated as Retryable
            except requests.exceptions.ConnectionError:
                raise RDStationException(
                    429,
                    {
                        "errors": {
                            "error_type": "RATE_LIMIT_EXCEDDED",
                            "error_message": "API usage limit exceeded",
                        }
                    },
                )

            # Is treated as Retryable
            except requests.exceptions.Timeout:
                raise RDStationException(
                    429,
                    {
                        "errors": {
                            "error_type": "RATE_LIMIT_EXCEDDED",
                            "error_message": "API usage limit exceeded",
                        }
                    },
                )
            except Exception as e:
                raise

        # return _call_request(method, url, data, headers)

        while True:
            response_data = _call_request(method, url, data, headers)

            yield response_data

            if response_data.get("has_more", False):
                url.replace(f"page={page}", f"page={page+1}")
                page += 1

            else:
                return response_data
                break
