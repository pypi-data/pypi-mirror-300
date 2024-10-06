import requests


class APIHandler:
    def __init__(self, base_url: str = None, api_key: str = None):
        _base_url = "https://prod-base.api.einmind.com:443"
        if base_url is not None:
            _base_url = base_url

        if not _base_url.startswith("http"):
            raise ValueError('Base url must be provided in the format of https://<ip or domain>:<port> or http://<ip or domain>:<port>')

        if not _base_url.endswith("/"):
            _base_url += "/"

        self.base_url = _base_url
        self.headers = self._init_headers(api_key=api_key)

    def _init_headers(self, api_key: str) -> dict:
        # Headers for the API requests
        headers = {
            'accept': 'application/json',
            'x-api-key': api_key,
            'Content-Type': 'application/json'
        }
        return headers

    def post(self, endpoint, payload):
        url = f"{self.base_url}{endpoint}"
        return requests.post(url, json=payload, headers=self.headers)

    def get(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        return requests.get(url, headers=self.headers)
