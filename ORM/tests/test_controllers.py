"""
Тести контролерів
"""
import pytest
from datetime import date


class TestTournamentController:
    """Тести контролера турнірів"""
    
    @pytest.mark.asyncio
    async def test_get_all_tournaments(self, db_session):
        """Тест отримання всіх турнірів"""
        from ORM.controllers import TournamentController
        from ORM.models import Tournaments
        
        # Створюємо тестові дані
        t1 = Tournaments(name="Tournament 1", start_date=date(2024, 1, 1))
        t2 = Tournaments(name="Tournament 2", start_date=date(2024, 2, 1))
        db_session.add_all([t1, t2])
        db_session.commit()
        
        # Тестуємо контролер
        tournaments = await TournamentController.get_all(db_session, skip=0, limit=10)
        assert len(tournaments) == 2
    
    @pytest.mark.asyncio
    async def test_create_tournament(self, db_session):
        """Тест створення турніру через контролер"""
        from ORM.controllers import TournamentController
        from ORM.schemas import TournamentBase
        
        tournament_data = TournamentBase(
            name="New Tournament",
            start_date=date(2024, 5, 1),
            end_date=date(2024, 5, 10)
        )
        
        tournament = await TournamentController.create(db_session, tournament_data)
        assert tournament.tournament_id is not None
        assert tournament.name == "New Tournament"
    
    @pytest.mark.asyncio
    async def test_get_tournament_by_id(self, db_session, sample_tournament):
        """Тест отримання турніру за ID"""
        from ORM.controllers import TournamentController
        
        tournament = await TournamentController.get_by_id(db_session, sample_tournament.tournament_id)
        assert tournament is not None
        assert tournament.tournament_id == sample_tournament.tournament_id


class TestTeamController:
    """Тести контролера команд"""
    
    @pytest.mark.asyncio
    async def test_get_all_teams(self, db_session):
        """Тест отримання всіх команд"""
        from ORM.controllers import TeamController
        from ORM.models import Teams
        
        team1 = Teams(name="Team Alpha")
        team2 = Teams(name="Team Beta")
        db_session.add_all([team1, team2])
        db_session.commit()
        
        teams = await TeamController.get_all(db_session, skip=0, limit=10)
        assert len(teams) == 2
    
    @pytest.mark.asyncio
    async def test_create_team(self, db_session):
        """Тест створення команди"""
        from ORM.controllers import TeamController
        from ORM.schemas import TeamBase
        
        team_data = TeamBase(name="New Team")
        team = await TeamController.create(db_session, team_data)
        
        assert team.team_id is not None
        assert team.name == "New Team"


class TestPlayerController:
    """Тести контролера гравців"""
    
    @pytest.mark.asyncio
    async def test_get_all_players(self, db_session, sample_team):
        """Тест отримання всіх гравців"""
        from ORM.controllers import PlayerController
        from ORM.models import Players
        
        p1 = Players(name="Player 1", nickname="P1", position="Carry", team_id=sample_team.team_id)
        p2 = Players(name="Player 2", nickname="P2", position="Mid", team_id=sample_team.team_id)
        db_session.add_all([p1, p2])
        db_session.commit()
        
        players = await PlayerController.get_all(db_session, skip=0, limit=10)
        assert len(players) == 2
    
    @pytest.mark.asyncio
    async def test_create_player(self, db_session, sample_team):
        """Тест створення гравця"""
        from ORM.controllers import PlayerController
        from ORM.schemas import PlayerBase
        
        player_data = PlayerBase(
            name="New Player",
            nickname="NP",
            position="Support",
            team_id=sample_team.team_id
        )
        
        player = await PlayerController.create(db_session, player_data)
        assert player.player_id is not None
        assert player.name == "New Player"


class TestHeroController:
    """Тести контролера героїв"""
    
    @pytest.mark.asyncio
    async def test_get_all_heroes(self, db_session):
        """Тест отримання всіх героїв"""
        from ORM.controllers import HeroController
        from ORM.models import Heroes
        
        h1 = Heroes(name="Hero 1", role="Carry", ultimate="Ultimate 1")
        h2 = Heroes(name="Hero 2", role="Support", ultimate="Ultimate 2")
        db_session.add_all([h1, h2])
        db_session.commit()
        
        heroes = await HeroController.get_all(db_session, skip=0, limit=10)
        assert len(heroes) == 2
    
    @pytest.mark.asyncio
    async def test_create_hero(self, db_session):
        """Тест створення героя"""
        from ORM.controllers import HeroController
        from ORM.schemas import HeroBase
        
        hero_data = HeroBase(
            name="New Hero",
            role="Nuker",
            ultimate="Big Boom"
        )
        
        hero = await HeroController.create(db_session, hero_data)
        assert hero.hero_id is not None
        assert hero.name == "New Hero"
