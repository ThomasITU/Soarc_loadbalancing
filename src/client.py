import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import config
import argparse

LOADBALANCER_ADDRESS = config.address 
class ResilientClient:
    def __init__(self, url, retries=3):
        self.url = url
        self.session = requests.Session()
        retries = Retry(total=retries, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
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
    parser = argparse.ArgumentParser(description='Process optional flag client.')
    parser.add_argument('-a', type=str, help='address of the loadbalancer default = "localhost"', dest='address')

    args = parser.parse_args()
    
    if args.address is not None:
        LOADBALANCER_ADDRESS = args.address
 
    client = ResilientClient(f"http://{LOADBALANCER_ADDRESS}:8080/?integer=21", 3)
    for i in range(0, config.number_of_client_requests):
        response = client.get()
        # print(response)
 