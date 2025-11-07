from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .schemas import *
from .models import *
from .crud import *

class BaseController:
    """Базовий клас для всіх контролерів"""
    @staticmethod
    def check_exists(item, detail: str):
        if not item:
            raise HTTPException(status_code=404, detail=detail)
        return item

class TournamentController:
    @staticmethod
    async def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[TournamentResponse]:
        return get_tournaments(db, skip=skip, limit=limit)

    @staticmethod
    async def create(db: Session, tournament: TournamentBase) -> TournamentResponse:
        return create_tournament(
            db,
            tournament.name,
            tournament.start_date,
            tournament.end_date,
            tournament.winner
        )

    @staticmethod
    async def get_by_id(db: Session, tournament_id: int) -> TournamentResponse:
        tournament = get_tournament(db, tournament_id)
        return BaseController.check_exists(tournament, "Турнір не знайдено")

class SeriesController:
    @staticmethod
    async def get_by_tournament(db: Session, tournament_id: int) -> List[SeriesResponse]:
        tournament = get_tournament(db, tournament_id)
        BaseController.check_exists(tournament, "Турнір не знайдено")
        return get_series_by_tournament(db, tournament_id)

    @staticmethod
    async def create(db: Session, tournament_id: int, series: SeriesBase) -> SeriesResponse:
        tournament = get_tournament(db, tournament_id)
        BaseController.check_exists(tournament, "Турнір не знайдено")
        return create_series(
            db,
            tournament_id,
            series.team1_id,
            series.team2_id
        )

class MatchController:
    @staticmethod
    async def get_by_series(db: Session, series_id: int) -> List[MatchResponse]:
        series = get_series(db, series_id)
        BaseController.check_exists(series, "Серію не знайдено")
        return get_matches_by_series(db, series_id)

    @staticmethod
    async def create(db: Session, match: MatchBase) -> MatchResponse:
        # Перевірка існування всіх зовнішніх ключів
        series = get_series(db, match.series_id)
        BaseController.check_exists(series, "Серію не знайдено")
        
        tournament = get_tournament(db, match.tournament_id)
        BaseController.check_exists(tournament, "Турнір не знайдено")
        
        team_radiant = get_team(db, match.team_radiant)
        BaseController.check_exists(team_radiant, "Команду Radiant не знайдено")
        
        team_dire = get_team(db, match.team_dire)
        BaseController.check_exists(team_dire, "Команду Dire не знайдено")
        
        winner = get_team(db, match.winner_id)
        BaseController.check_exists(winner, "Команду-переможця не знайдено")

        return create_match(
            db,
            match.series_id,
            match.tournament_id,
            match.team_radiant,
            match.team_dire,
            match.winner_id
        )

class TeamController:
    @staticmethod
    async def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[TeamResponse]:
        return get_teams(db, skip=skip, limit=limit)

    @staticmethod
    async def create(db: Session, team: TeamBase) -> TeamResponse:
        return create_team(db, team.name)

    @staticmethod
    async def get_by_id(db: Session, team_id: int) -> TeamResponse:
        team = get_team(db, team_id)
        return BaseController.check_exists(team, "Команду не знайдено")

class PlayerController:
    @staticmethod
    async def get_by_team(db: Session, team_id: int) -> List[PlayerResponse]:
        team = get_team(db, team_id)
        BaseController.check_exists(team, "Команду не знайдено")
        return get_players_by_team(db, team_id)

    @staticmethod
    async def create(db: Session, team_id: int, player: PlayerBase) -> PlayerResponse:
        team = get_team(db, team_id)
        BaseController.check_exists(team, "Команду не знайдено")
        return create_player(
            db,
            player.name,
            player.nickname,
            player.position,
            team_id
        )

class HeroController:
    @staticmethod
    async def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[HeroResponse]:
        return get_heroes(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: Session, hero_id: int) -> HeroResponse:
        hero = get_hero(db, hero_id)
        return BaseController.check_exists(hero, "Героя не знайдено")

class StatisticsController:
    @staticmethod
    async def get_by_player(db: Session, player_id: int) -> List[StatisticResponse]:
        player = get_player(db, player_id)
        BaseController.check_exists(player, "Гравця не знайдено")
        return get_player_statistics_records(db, player_id)

    @staticmethod
    async def get_by_match(db: Session, match_id: int) -> List[StatisticResponse]:
        match = get_match(db, match_id)
        BaseController.check_exists(match, "Матч не знайдено")
        return get_match_statistics_records(db, match_id)

    @staticmethod
    async def get_by_hero(db: Session, hero_id: int) -> List[StatisticResponse]:
        hero = get_hero(db, hero_id)
        BaseController.check_exists(hero, "Героя не знайдено")
        return get_hero_statistics_records(db, hero_id)

    @staticmethod
    async def create(db: Session, stat: StatisticBase) -> StatisticResponse:
        # Перевірка існування всіх зовнішніх ключів
        player = get_player(db, stat.player_id)
        BaseController.check_exists(player, "Гравця не знайдено")
        
        match = get_match(db, stat.match_id)
        BaseController.check_exists(match, "Матч не знайдено")
        
        hero = get_hero(db, stat.hero_id)
        BaseController.check_exists(hero, "Героя не знайдено")

        return create_statistics_record(
            db,
            stat.player_id,
            stat.match_id,
            stat.hero_id,
            stat.kills,
            stat.deaths,
            stat.assists,
            stat.damage,
            stat.roshan_kills,
            stat.towers_kills
        )

class PrizeController:
    @staticmethod
    async def get_by_team(db: Session, team_id: int) -> List[PrizeResponse]:
        team = get_team(db, team_id)
        BaseController.check_exists(team, "Команду не знайдено")
        return get_prizes_by_team(db, team_id)

    @staticmethod
    async def create(db: Session, prize: PrizeBase) -> PrizeResponse:
        team = get_team(db, prize.team_id)
        BaseController.check_exists(team, "Команду не знайдено")
        
        tournament = get_tournament(db, prize.tournament_id)
        BaseController.check_exists(tournament, "Турнір не знайдено")

        return create_prize(
            db,
            prize.team_id,
            prize.tournament_id,
            prize.amount,
            prize.position
        )