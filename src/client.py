import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import config

class ResilientClient:
    def __init__(self, url, retries=3):
        self.url = url
        self.session = requests.Session()
        retries = Retry(total=retries, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))

    def get(self):
        try:
            response = self.session.get(self.url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except requests.exceptions.ConnectionError as conn_err:
            print(f'Connection error occurred: {conn_err}')
        except requests.exceptions.Timeout as timeout_err:
            print(f'Timeout error occurred: {timeout_err}')
        except requests.exceptions.RequestException as err:
            print(f'An error occurred: {err}')

if __name__ == "__main__":
    client = ResilientClient("http://localhost:8080/?integer=21", 3)
    for i in range(0, config.number_of_client_requests):
        response = client.get()
        print(response)
