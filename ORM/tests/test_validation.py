"""
Тести валідаторів
"""
import pytest
from fastapi import HTTPException


class TestValidators:
    """Тести кастомних валідаторів"""
    
    def test_validate_team_exists_success(self, db_session, sample_team):
        """Тест успішної валідації існування команди"""
        from ORM.validation import validate_team_exists
        
        # Не має викинути помилку
        validate_team_exists(db_session, sample_team.team_id)
    
    def test_validate_team_exists_fail(self, db_session):
        """Тест валідації неіснуючої команди"""
        from ORM.validation import validate_team_exists, ValidationError
        
        with pytest.raises(ValidationError) as exc_info:
            validate_team_exists(db_session, 99999)
        assert "не знайдена" in str(exc_info.value.detail)
    
    def test_validate_unique_team_name_success(self, db_session):
        """Тест валідації унікальності назви команди (успіх)"""
        from ORM.validation import validate_unique_team_name
        
        # Не має викинути помилку для нової назви
        validate_unique_team_name(db_session, "Unique Team Name")
    
    def test_validate_unique_team_name_fail(self, db_session, sample_team):
        """Тест валідації унікальності назви команди (помилка)"""
        from ORM.validation import validate_unique_team_name, ValidationError
        
        with pytest.raises(ValidationError) as exc_info:
            validate_unique_team_name(db_session, sample_team.name)
        assert "вже існує" in str(exc_info.value.detail)
    
    def test_validate_series_teams_success(self, db_session):
        """Тест валідації команд у серії (успіх)"""
        from ORM.validation import validate_series_teams
        from ORM.models import Teams
        
        team1 = Teams(name="Team 1")
        team2 = Teams(name="Team 2")
        db_session.add_all([team1, team2])
        db_session.commit()
        
        # Не має викинути помилку
        validate_series_teams(db_session, team1.team_id, team2.team_id, team1.team_id)
    
    def test_validate_series_teams_same_teams(self, db_session, sample_team):
        """Тест валідації серії з однаковими командами"""
        from ORM.validation import validate_series_teams, ValidationError
        
        with pytest.raises(ValidationError) as exc_info:
            validate_series_teams(db_session, sample_team.team_id, sample_team.team_id)
        assert "різними" in str(exc_info.value.detail)
    
    def test_validate_match_teams_success(self, db_session):
        """Тест валідації команд у матчі (успіх)"""
        from ORM.validation import validate_match_teams
        from ORM.models import Teams
        
        radiant = Teams(name="Radiant")
        dire = Teams(name="Dire")
        db_session.add_all([radiant, dire])
        db_session.commit()
        
        # Не має викинути помилку
        validate_match_teams(db_session, radiant.team_id, dire.team_id, radiant.team_id)
    
    def test_validate_match_teams_same_teams(self, db_session, sample_team):
        """Тест валідації матчу з однаковими командами"""
        from ORM.validation import validate_match_teams, ValidationError
        
        with pytest.raises(ValidationError) as exc_info:
            validate_match_teams(db_session, sample_team.team_id, sample_team.team_id, sample_team.team_id)
        assert "різними" in str(exc_info.value.detail)
    
    def test_validate_player_exists_success(self, db_session, sample_player):
        """Тест валідації існування гравця"""
        from ORM.validation import validate_player_exists
        
        validate_player_exists(db_session, sample_player.player_id)
    
    def test_validate_hero_exists_success(self, db_session, sample_hero):
        """Тест валідації існування героя"""
        from ORM.validation import validate_hero_exists
        
        validate_hero_exists(db_session, sample_hero.hero_id)
    
    def test_validate_tournament_exists_success(self, db_session, sample_tournament):
        """Тест валідації існування турніру"""
        from ORM.validation import validate_tournament_exists
        
        validate_tournament_exists(db_session, sample_tournament.tournament_id)


class TestSchemaValidation:
    """Тести Pydantic схем валідації"""
    
    def test_player_position_validation(self):
        """Тест валідації позиції гравця"""
        from ORM.schemas import PlayerBase
        from pydantic import ValidationError
        
        # Валідна позиція
        player = PlayerBase(
            name="Test Player",
            nickname="TP",
            position="Carry",
            team_id=1
        )
        assert player.position == "Carry"
        
        # Невалідна позиція
        with pytest.raises(ValidationError):
            PlayerBase(
                name="Test Player",
                nickname="TP",
                position="InvalidPosition",
                team_id=1
            )
    
    def test_hero_role_validation(self):
        """Тест валідації ролі героя"""
        from ORM.schemas import HeroBase
        from pydantic import ValidationError
        
        # Валідна роль
        hero = HeroBase(name="Test Hero", role="Carry", ultimate="Test")
        assert hero.role == "Carry"
        
        # Невалідна роль
        with pytest.raises(ValidationError):
            HeroBase(name="Test Hero", role="InvalidRole", ultimate="Test")
    
    def test_tournament_dates_validation(self):
        """Тест валідації дат турніру"""
        from ORM.schemas import TournamentBase
        from pydantic import ValidationError
        from datetime import date
        
        # Валідні дати
        tournament = TournamentBase(
            name="Test",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 10)
        )
        assert tournament.start_date < tournament.end_date
        
        # Невалідні дати (end раніше start)
        with pytest.raises(ValidationError):
            TournamentBase(
                name="Test",
                start_date=date(2024, 1, 10),
                end_date=date(2024, 1, 1)
            )
    
    def test_statistics_kills_validation(self):
        """Тест валідації кількості вбивств"""
        from ORM.schemas import StatisticBase
        from pydantic import ValidationError
        
        # Валідна кількість
        stat = StatisticBase(
            player_id=1,
            match_id=1,
            hero_id=1,
            kills=50
        )
        assert stat.kills == 50
        
        # Невалідна кількість (більше 100)
        with pytest.raises(ValidationError):
            StatisticBase(
                player_id=1,
                match_id=1,
                hero_id=1,
                kills=150
            )
    
    def test_series_score_validation(self):
        """Тест валідації рахунку серії"""
        from ORM.schemas import SeriesBase
        from pydantic import ValidationError
        
        # Валідний рахунок
        series = SeriesBase(
            tournament_id=1,
            team1_id=1,
            team2_id=2,
            score_team1=2,
            score_team2=1
        )
        assert series.score_team1 == 2
        
        # Невалідний рахунок (більше 3)
        with pytest.raises(ValidationError):
            SeriesBase(
                tournament_id=1,
                team1_id=1,
                team2_id=2,
                score_team1=5,
                score_team2=1
            )
