import pytest
import requests
import json

def test_get_response_success(monkeypatch):
    ITEMS_PATH = "tests/fixtures/items.json"
    class MockResponse:
        def __init__(self):
            self.status_code = 200
            self.url = "https://deliver.kontent.ai/project_id/items"
            self.headers = {'blaa': '1234'}

        def json(self):
            with open(ITEMS_PATH) as f:
                data = json.load(f)
            return data

    def mock_get(url):
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
    assert get_items_request() == (200, 'about_us')


def get_items_request():
    r = requests.get("http://httpbin.org/get")

    if r.status_code == 200:
        response_data = r.json()
        return r.status_code, response_data["items"][0]["system"]["codename"]    
    else:
        return r.status_code, ""



#test_get_content_items
    # assert name
    # codename
    # id
    # languages
    # etc. etc.