import requests
import json

def test_players():
    response = requests.get('http://127.0.0.1:8000/spelers/me')
    assert response.status_code == 200
    response_dictionary = json.loads(response.text)

def test_player():
    response = requests.get('http://127.0.0.1:8000/spelers')
    assert response.status_code == 200
    response_dictionary = json.loads(response.text)


def test_player_id():
    response = requests.get('http://127.0.0.1:8000/spelers/{speler_id}')
    assert response.status_code == 200
    response_dictionary = json.loads(response.text)


def test_compititie():
    response = requests.get('http://127.0.0.1:8000/compititie/')
    assert response.status_code == 200
    response_dictionary = json.loads(response.text)


def test_beker():
    response = requests.get('http://127.0.0.1:8000/beker/')
    assert response.status_code == 200
    response_dictionary = json.loads(response.text)
