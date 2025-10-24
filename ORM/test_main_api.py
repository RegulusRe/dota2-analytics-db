# test_main_api.py

import pytest
from fastapi.testclient import TestClient
from main_api import app

client = TestClient(app)

@pytest.fixture(scope="module")
def test_player():
    # Створюємо гравця для тестів
    new_player_data = {
        "name": "Pytest Player",
        "nickname": "PytestNick",
        "position": "Support",
        "team_id": 9565  # Team Spirit
    }
    response = client.post("/players/", json=new_player_data)
    assert response.status_code == 200
    player = response.json()
    yield player
    # Видаляємо гравця після тестів
    client.delete(f"/players/{player['player_id']}")

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Ласкаво просимо до Dota 2 API!"}

def test_create_player():
    new_player_data = {
        "name": "Test API Player",
        "nickname": "TestAPI",
        "position": "Mid",
        "team_id": 9565
    }
    response = client.post("/players/", json=new_player_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_player_data["name"]
    assert data["nickname"] == new_player_data["nickname"]
    assert data["team_id"] == new_player_data["team_id"]
    # Видаляємо гравця після тесту
    client.delete(f"/players/{data['player_id']}")

def test_get_player(test_player):
    player_id = test_player["player_id"]
    response = client.get(f"/players/{player_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_player["name"]
    assert data["nickname"] == test_player["nickname"]

def test_get_player_not_found():
    response = client.get("/players/999999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Гравця не знайдено"}

def test_get_players():
    response = client.get("/players/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_update_player(test_player):
    player_id = test_player["player_id"]
    update_data = {"nickname": "UpdatedByPytest"}
    response = client.put(f"/players/{player_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["nickname"] == "UpdatedByPytest"

def test_update_player_not_found():
    update_data = {"nickname": "ShouldFail"}
    response = client.put("/players/999999999", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Гравця не знайдено"}

def test_delete_player(test_player):
    player_id = test_player["player_id"]
    response = client.delete(f"/players/{player_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Гравця видалено"}

def test_delete_player_not_found():
    response = client.delete("/players/999999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Гравця не знайдено"}