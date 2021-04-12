import requests
from requests.exceptions import Timeout, RequestException 

class RequestManager:
    @staticmethod
    def get_request(client, url, headers = {}):
        if hasattr(client.client_options, "timeout"):
            timeout_option = client.client_options.timeout
        else:
            timeout_option = (2,5)
        
        if hasattr(client.client_options, "preview"):
            auth_token = f"Bearer {client.client_options.preview_api_key}"
            headers["Authorization"] = auth_token
        r = requests.get(url, timeout=timeout_option, headers=headers)

        if hasattr(client.client_options, "secured"):
            auth_token = f"Bearer {client.client_options.secured_api_key}"
            headers["Authorization"] = auth_token

        r = requests.get(url, timeout=timeout_option, headers=headers)
              
        print("REAL REQUEST MADE TO API.")

        try:   
            r.raise_for_status()
        except Timeout as e:
            print(f"request timed out with: {e}.")
        except RequestException as e:
            print(f"request failed with error: {e}")

        return r


