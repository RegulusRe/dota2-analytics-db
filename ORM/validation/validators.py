"""
Кастомні валідатори для бізнес-логіки ORM
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .models import Teams, Players, Heroes, Tournaments, Series, Matches


class ValidationError(HTTPException):
    """Базовий клас для помилок валідації"""
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def validate_team_exists(db: Session, team_id: int) -> None:
    """Перевіряє чи існує команда"""
    team = db.query(Teams).filter(Teams.team_id == team_id).first()
    if not team:
        raise ValidationError(f"Команда з ID {team_id} не знайдена")


def validate_player_exists(db: Session, player_id: int) -> None:
    """Перевіряє чи існує гравець"""
    player = db.query(Players).filter(Players.player_id == player_id).first()
    if not player:
        raise ValidationError(f"Гравець з ID {player_id} не знайдений")


def validate_hero_exists(db: Session, hero_id: int) -> None:
    """Перевіряє чи існує герой"""
    hero = db.query(Heroes).filter(Heroes.hero_id == hero_id).first()
    if not hero:
        raise ValidationError(f"Герой з ID {hero_id} не знайдений")


def validate_tournament_exists(db: Session, tournament_id: int) -> None:
    """Перевіряє чи існує турнір"""
    tournament = db.query(Tournaments).filter(Tournaments.tournament_id == tournament_id).first()
    if not tournament:
        raise ValidationError(f"Турнір з ID {tournament_id} не знайдений")


def validate_series_exists(db: Session, series_id: int) -> None:
    """Перевіряє чи існує серія"""
    series = db.query(Series).filter(Series.series_id == series_id).first()
    if not series:
        raise ValidationError(f"Серія з ID {series_id} не знайдена")


def validate_match_exists(db: Session, match_id: int) -> None:
    """Перевіряє чи існує матч"""
    match = db.query(Matches).filter(Matches.match_id == match_id).first()
    if not match:
        raise ValidationError(f"Матч з ID {match_id} не знайдений")


def validate_unique_team_name(db: Session, name: str, exclude_id: int = None) -> None:
    """Перевіряє унікальність назви команди"""
    query = db.query(Teams).filter(Teams.name == name)
    if exclude_id:
        query = query.filter(Teams.team_id != exclude_id)
    if query.first():
        raise ValidationError(f"Команда з назвою '{name}' вже існує")


def validate_unique_hero_name(db: Session, name: str, exclude_id: int = None) -> None:
    """Перевіряє унікальність імені героя"""
    query = db.query(Heroes).filter(Heroes.name == name)
    if exclude_id:
        query = query.filter(Heroes.hero_id != exclude_id)
    if query.first():
        raise ValidationError(f"Герой з ім'ям '{name}' вже існує")


def validate_series_teams(db: Session, team1_id: int, team2_id: int, winner_id: int = None) -> None:
    """Перевіряє коректність команд в серії"""
    # Перевірка існування команд
    validate_team_exists(db, team1_id)
    validate_team_exists(db, team2_id)
    
    # Команди мають бути різними
    if team1_id == team2_id:
        raise ValidationError("Команди в серії мають бути різними")
    
    # Переможець має бути однією з команд
    if winner_id and winner_id not in [team1_id, team2_id]:
        raise ValidationError("Переможець має бути однією з команд серії")


def validate_match_teams(db: Session, team_radiant: int, team_dire: int, winner_id: int) -> None:
    """Перевіряє коректність команд в матчі"""
    # Перевірка існування команд
    validate_team_exists(db, team_radiant)
    validate_team_exists(db, team_dire)
    validate_team_exists(db, winner_id)
    
    # Команди мають бути різними
    if team_radiant == team_dire:
        raise ValidationError("Команди Radiant і Dire мають бути різними")
    
    # Переможець має бути Radiant або Dire
    if winner_id not in [team_radiant, team_dire]:
        raise ValidationError("Переможець має бути командою Radiant або Dire")


def validate_series_belongs_to_tournament(db: Session, series_id: int, tournament_id: int) -> None:
    """Перевіряє чи належить серія турніру"""
    series = db.query(Series).filter(Series.series_id == series_id).first()
    if not series:
        raise ValidationError(f"Серія з ID {series_id} не знайдена")
    if series.tournament_id != tournament_id:
        raise ValidationError(f"Серія {series_id} не належить турніру {tournament_id}")


def validate_player_in_team(db: Session, player_id: int, team_id: int) -> None:
    """Перевіряє чи гравець належить команді"""
    player = db.query(Players).filter(Players.player_id == player_id).first()
    if not player:
        raise ValidationError(f"Гравець з ID {player_id} не знайдений")
    if player.team_id != team_id:
        raise ValidationError(f"Гравець {player_id} не належить команді {team_id}")


def validate_statistics_data(db: Session, player_id: int, match_id: int, hero_id: int) -> None:
    """Валідація даних статистики"""
    validate_player_exists(db, player_id)
    validate_match_exists(db, match_id)
    validate_hero_exists(db, hero_id)
    
    # Перевірка чи немає дублікату статистики
    from .models import Statistics
    existing = db.query(Statistics).filter(
        Statistics.player_id == player_id,
        Statistics.match_id == match_id
    ).first()
    if existing:
        raise ValidationError(f"Статистика для гравця {player_id} в матчі {match_id} вже існує")


def validate_prize_data(db: Session, team_id: int, tournament_id: int, position: int) -> None:
    """Валідація даних призу"""
    validate_team_exists(db, team_id)
    validate_tournament_exists(db, tournament_id)
    
    # Перевірка чи немає дублікату призу
    from .models import Prizes
    existing = db.query(Prizes).filter(
        Prizes.tournament_id == tournament_id,
        Prizes.team_id == team_id
    ).first()
    if existing:
        raise ValidationError(f"Приз для команди {team_id} в турнірі {tournament_id} вже існує")
