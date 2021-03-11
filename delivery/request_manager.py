import requests
from requests.exceptions import Timeout, RequestException 

class RequestManager:
    @staticmethod
    def get_request(client, url):
        if hasattr(client.client_options, "timeout"):
            timeout_option = client.client_options.timeout
        else:
            timeout_option = (2,5)
        
        r = requests.get(url, timeout=timeout_option)
        try:   
            r.raise_for_status()
        except Timeout as e:
            print(f"request timed out with: {e}.")
        except RequestException as e:
            print(f"request failed with error: {e}")

        return r


