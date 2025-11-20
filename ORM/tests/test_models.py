"""
Юніт тести для моделей
"""
import pytest
from datetime import date


class TestTeamModel:
    """Тести моделі Teams"""
    
    def test_create_team(self, db_session):
        """Тест створення команди"""
        from ORM.models import Teams
        
        team = Teams(name="Team Secret")
        db_session.add(team)
        db_session.commit()
        
        assert team.team_id is not None
        assert team.name == "Team Secret"
    
    def test_team_name_unique(self, db_session):
        """Тест унікальності назви команди"""
        from ORM.models import Teams
        from sqlalchemy.exc import IntegrityError
        
        team1 = Teams(name="Unique Team")
        db_session.add(team1)
        db_session.commit()
        
        team2 = Teams(name="Unique Team")
        db_session.add(team2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()


class TestPlayerModel:
    """Тести моделі Players"""
    
    def test_create_player(self, db_session, sample_team):
        """Тест створення гравця"""
        from ORM.models import Players
        
        player = Players(
            name="John Doe",
            nickname="JD",
            position="Mid",
            team_id=sample_team.team_id
        )
        db_session.add(player)
        db_session.commit()
        
        assert player.player_id is not None
        assert player.name == "John Doe"
        assert player.nickname == "JD"
        assert player.position == "Mid"
        assert player.team_id == sample_team.team_id
    
    def test_player_team_relationship(self, db_session, sample_player, sample_team):
        """Тест зв'язку гравець-команда"""
        assert sample_player.team.team_id == sample_team.team_id
        assert sample_player.team.name == sample_team.name


class TestHeroModel:
    """Тести моделі Heroes"""
    
    def test_create_hero(self, db_session):
        """Тест створення героя"""
        from ORM.models import Heroes
        
        hero = Heroes(
            name="Pudge",
            role="Disabler",
            ultimate="Dismember"
        )
        db_session.add(hero)
        db_session.commit()
        
        assert hero.hero_id is not None
        assert hero.name == "Pudge"
        assert hero.role == "Disabler"
    
    def test_hero_name_unique(self, db_session):
        """Тест унікальності імені героя"""
        from ORM.models import Heroes
        from sqlalchemy.exc import IntegrityError
        
        hero1 = Heroes(name="Invoker", role="Nuker", ultimate="Chaos Meteor")
        db_session.add(hero1)
        db_session.commit()
        
        hero2 = Heroes(name="Invoker", role="Nuker", ultimate="Chaos Meteor")
        db_session.add(hero2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()


class TestTournamentModel:
    """Тести моделі Tournaments"""
    
    def test_create_tournament(self, db_session):
        """Тест створення турніру"""
        from ORM.models import Tournaments
        
        tournament = Tournaments(
            name="The International 2024",
            start_date=date(2024, 10, 1),
            end_date=date(2024, 10, 15),
            winner="Team Secret"
        )
        db_session.add(tournament)
        db_session.commit()
        
        assert tournament.tournament_id is not None
        assert tournament.name == "The International 2024"
        assert tournament.start_date == date(2024, 10, 1)
        assert tournament.end_date == date(2024, 10, 15)


class TestSeriesModel:
    """Тести моделі Series"""
    
    def test_create_series(self, db_session, sample_tournament):
        """Тест створення серії"""
        from ORM.models import Series, Teams
        
        team1 = Teams(name="Team A")
        team2 = Teams(name="Team B")
        db_session.add_all([team1, team2])
        db_session.commit()
        
        series = Series(
            tournament_id=sample_tournament.tournament_id,
            team1_id=team1.team_id,
            team2_id=team2.team_id,
            winner_id=team1.team_id
        )
        db_session.add(series)
        db_session.commit()
        
        assert series.series_id is not None
        assert series.tournament_id == sample_tournament.tournament_id
        assert series.winner_id == team1.team_id


class TestMatchModel:
    """Тести моделі Matches"""
    
    def test_create_match(self, db_session, sample_tournament):
        """Тест створення матчу"""
        from ORM.models import Matches, Teams, Series
        
        team_radiant = Teams(name="Radiant Team")
        team_dire = Teams(name="Dire Team")
        db_session.add_all([team_radiant, team_dire])
        db_session.commit()
        
        series = Series(
            tournament_id=sample_tournament.tournament_id,
            team1_id=team_radiant.team_id,
            team2_id=team_dire.team_id
        )
        db_session.add(series)
        db_session.commit()
        
        match = Matches(
            series_id=series.series_id,
            tournament_id=sample_tournament.tournament_id,
            team_radiant=team_radiant.team_id,
            team_dire=team_dire.team_id,
            winner_id=team_radiant.team_id
        )
        db_session.add(match)
        db_session.commit()
        
        assert match.match_id is not None
        assert match.winner_id == team_radiant.team_id


class TestStatisticsModel:
    """Тести моделі Statistics"""
    
    def test_create_statistics(self, db_session, sample_player, sample_hero, sample_tournament):
        """Тест створення статистики"""
        from ORM.models import Statistics, Matches, Teams, Series
        
        team1 = Teams(name="Team X")
        team2 = Teams(name="Team Y")
        db_session.add_all([team1, team2])
        db_session.commit()
        
        series = Series(
            tournament_id=sample_tournament.tournament_id,
            team1_id=team1.team_id,
            team2_id=team2.team_id
        )
        db_session.add(series)
        db_session.commit()
        
        match = Matches(
            series_id=series.series_id,
            tournament_id=sample_tournament.tournament_id,
            team_radiant=team1.team_id,
            team_dire=team2.team_id,
            winner_id=team1.team_id
        )
        db_session.add(match)
        db_session.commit()
        
        stat = Statistics(
            player_id=sample_player.player_id,
            match_id=match.match_id,
            hero_id=sample_hero.hero_id,
            kills=10,
            deaths=2,
            assists=15,
            damage=25000
        )
        db_session.add(stat)
        db_session.commit()
        
        assert stat.stat_id is not None
        assert stat.kills == 10
        assert stat.deaths == 2
        assert stat.assists == 15
