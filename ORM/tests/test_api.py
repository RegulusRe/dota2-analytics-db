"""
Інтеграційні тести API endpoints
"""
import pytest


class TestTeamsAPI:
    """Тести API команд"""
    
    def test_get_all_teams(self, client):
        """Тест отримання всіх команд"""
        response = client.get("/teams")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_team(self, client):
        """Тест створення команди"""
        team_data = {"name": "New Team"}
        response = client.post("/teams", json=team_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Team"
        assert "team_id" in data
    
    def test_create_team_validation_error(self, client):
        """Тест валідації при створенні команди"""
        team_data = {"name": "A"}  # Занадто коротка назва
        response = client.post("/teams", json=team_data)
        assert response.status_code == 422
    
    def test_get_team_by_id(self, client, sample_team):
        """Тест отримання команди за ID"""
        response = client.get(f"/teams/{sample_team.team_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["team_id"] == sample_team.team_id
        assert data["name"] == sample_team.name
    
    def test_get_team_not_found(self, client):
        """Тест отримання неіснуючої команди"""
        response = client.get("/teams/99999")
        assert response.status_code == 404
    
    def test_update_team(self, client, sample_team):
        """Тест оновлення команди"""
        update_data = {"name": "Updated Team"}
        response = client.put(f"/teams/{sample_team.team_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Team"
    
    def test_delete_team(self, client, sample_team):
        """Тест видалення команди"""
        response = client.delete(f"/teams/{sample_team.team_id}")
        assert response.status_code == 200
        
        # Перевірка що команда видалена
        get_response = client.get(f"/teams/{sample_team.team_id}")
        assert get_response.status_code == 404


class TestPlayersAPI:
    """Тести API гравців"""
    
    def test_get_all_players(self, client):
        """Тест отримання всіх гравців"""
        response = client.get("/players")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_player(self, client, sample_team):
        """Тест створення гравця"""
        player_data = {
            "name": "John Doe",
            "nickname": "JD",
            "position": "Carry",
            "team_id": sample_team.team_id
        }
        response = client.post("/players", json=player_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["nickname"] == "JD"
        assert "player_id" in data
    
    def test_create_player_invalid_position(self, client, sample_team):
        """Тест створення гравця з невалідною позицією"""
        player_data = {
            "name": "John Doe",
            "nickname": "JD",
            "position": "InvalidPosition",
            "team_id": sample_team.team_id
        }
        response = client.post("/players", json=player_data)
        assert response.status_code == 422
    
    def test_get_player_by_id(self, client, sample_player):
        """Тест отримання гравця за ID"""
        response = client.get(f"/players/{sample_player.player_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["player_id"] == sample_player.player_id
        assert data["name"] == sample_player.name
    
    def test_update_player(self, client, sample_player):
        """Тест оновлення гравця"""
        update_data = {"nickname": "NewNick"}
        response = client.put(f"/players/{sample_player.player_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nickname"] == "NewNick"
    
    def test_delete_player(self, client, sample_player):
        """Тест видалення гравця"""
        response = client.delete(f"/players/{sample_player.player_id}")
        assert response.status_code == 200


class TestHeroesAPI:
    """Тести API героїв"""
    
    def test_get_all_heroes(self, client):
        """Тест отримання всіх героїв"""
        response = client.get("/heroes")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_hero(self, client):
        """Тест створення героя"""
        hero_data = {
            "name": "Pudge",
            "role": "Disabler",
            "ultimate": "Dismember"
        }
        response = client.post("/heroes", json=hero_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Pudge"
        assert data["role"] == "Disabler"
    
    def test_create_hero_invalid_role(self, client):
        """Тест створення героя з невалідною роллю"""
        hero_data = {
            "name": "TestHero",
            "role": "InvalidRole",
            "ultimate": "Test Ultimate"
        }
        response = client.post("/heroes", json=hero_data)
        assert response.status_code == 422
    
    def test_get_hero_by_id(self, client, sample_hero):
        """Тест отримання героя за ID"""
        response = client.get(f"/heroes/{sample_hero.hero_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["hero_id"] == sample_hero.hero_id


class TestTournamentsAPI:
    """Тести API турнірів"""
    
    def test_get_all_tournaments(self, client):
        """Тест отримання всіх турнірів"""
        response = client.get("/tournaments")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_tournament(self, client):
        """Тест створення турніру"""
        tournament_data = {
            "name": "Test Tournament",
            "start_date": "2024-01-01",
            "end_date": "2024-01-10"
        }
        response = client.post("/tournaments", json=tournament_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Tournament"
    
    def test_create_tournament_invalid_dates(self, client):
        """Тест створення турніру з невалідними датами"""
        tournament_data = {
            "name": "Test Tournament",
            "start_date": "2024-01-10",
            "end_date": "2024-01-01"  # End before start
        }
        response = client.post("/tournaments", json=tournament_data)
        assert response.status_code == 422
    
    def test_get_tournament_by_id(self, client, sample_tournament):
        """Тест отримання турніру за ID"""
        response = client.get(f"/tournaments/{sample_tournament.tournament_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["tournament_id"] == sample_tournament.tournament_id


class TestAuthAPI:
    """Тести API авторизації"""
    
    def test_register_user(self, client):
        """Тест реєстрації користувача"""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123"
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data
    
    def test_register_duplicate_username(self, client, test_user):
        """Тест реєстрації з існуючим username"""
        user_data = {
            "username": "testuser",
            "email": "another@example.com",
            "password": "password123"
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 400
    
    def test_login_success(self, client, test_user):
        """Тест успішного входу"""
        login_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        response = client.post("/auth/login", data=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self, client, test_user):
        """Тест входу з неправильним паролем"""
        login_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", data=login_data)
        assert response.status_code == 401
    
    def test_get_current_user(self, client, auth_headers):
        """Тест отримання поточного користувача"""
        response = client.get("/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
    
    def test_get_current_user_no_token(self, client):
        """Тест отримання користувача без токена"""
        response = client.get("/auth/me")
        assert response.status_code == 401


class TestAPIValidation:
    """Тести валідації API"""
    
    def test_create_series_same_teams(self, client, sample_tournament):
        """Тест створення серії з однаковими командами"""
        from ORM.models import Teams
        team = Teams(name="Solo Team")
        # Цей тест перевірить валідацію на рівні Pydantic
        series_data = {
            "tournament_id": sample_tournament.tournament_id,
            "team1_id": 1,
            "team2_id": 1,  # Same as team1
            "score_team1": 0,
            "score_team2": 0
        }
        response = client.post("/series", json=series_data)
        # Має бути помилка валідації
        assert response.status_code in [400, 422]
    
    def test_statistics_invalid_kills(self, client, sample_player, sample_hero):
        """Тест створення статистики з невалідним числом вбивств"""
        stat_data = {
            "player_id": sample_player.player_id,
            "match_id": 1,
            "hero_id": sample_hero.hero_id,
            "kills": 150,  # Більше максимуму (100)
            "deaths": 5,
            "assists": 10,
            "damage": 20000
        }
        response = client.post("/statistics", json=stat_data)
        assert response.status_code == 422
