import requests
import pytest

def test_get_transcript():
    url = 'http://127.0.0.1:5000/api/transcript'
    data = {'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert 'text' in response.json()[0]
    assert 'start' in response.json()[0]
    assert 'duration' in response.json()[0]