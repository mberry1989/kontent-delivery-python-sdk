import requests
from requests.adapters import Retry
from requests.exceptions import Timeout, RequestException
from requests.sessions import HTTPAdapter


class RequestManager:
    @staticmethod
    def get_request(client, url, headers={}):
        if hasattr(client.client_options, "timeout"):
            timeout_option = client.client_options.timeout
        else:
            timeout_option = (2, 5)

        if hasattr(client.client_options, "preview"):
            auth_token = f"Bearer {client.client_options.preview_api_key}"
            headers["Authorization"] = auth_token

        if hasattr(client.client_options, "secured"):
            auth_token = f"Bearer {client.client_options.secured_api_key}"
            headers["Authorization"] = auth_token

        retry_strategy = Retry(
            total=6,
            backoff_factor=1,
            status_forcelist=[408, 429, 500, 502, 503, 504])

        if hasattr(client.client_options, "retry_attempts"):
            retry_strategy.total = client.client_options.retry_attempts

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("https://", adapter)

        response = session.get(url, timeout=timeout_option, headers=headers)

        try:
            response.raise_for_status()
        except Timeout as e:
            print(f"request timed out with: {e}.")
        except RequestException as e:
            print(f"request failed with error: {e}")

        return response
