from sqlalchemy.orm import Session
from models import Players, Teams, Heroes, Statistics, Tournaments, Series, Matches, Prizes
from typing import List, Optional
from datetime import date
# ====================== CREATE ======================

def create_player(db: Session, name: str, nickname: str, position: str, team_id: int):
    """Створення нового гравця."""
    db_player = Players(
        name=name,
        nickname=nickname,
        position=position,
        team_id=team_id
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def create_team(db: Session, name: str):
    """Створння нову команду."""
    db_team = Teams(name=name)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def create_hero(db: Session, name: str, role: str, ultimate: str):
    """Створння нового героя."""
    db_hero = Heroes(name=name, role=role, ultimate=ultimate)
    db.add(db_hero)
    db.commit()
    db.refresh(db_hero)
    return db_hero

def create_statistics_record(
    db: Session,
    player_id: int,
    match_id: int,
    hero_id: int,
    kills: int = 0,
    deaths: int = 0,
    assists: int = 0,
    damage: int = 0,
    roshan_kills: int = 0,
    towers_kills: int = 0
):
    """Створення нового запису статистики."""
    db_stat = Statistics(
        player_id=player_id,
        match_id=match_id,
        hero_id=hero_id,
        kills=kills,
        deaths=deaths,
        assists=assists,
        damage=damage,
        roshan_kills=roshan_kills,
        towers_kills=towers_kills
    )
    db.add(db_stat)
    db.commit()
    db.refresh(db_stat)
    return db_stat

# ====================== READ ======================

def get_player(db: Session, player_id: int):
    """Отримння гравця за ID."""
    return db.query(Players).filter(Players.player_id == player_id).first()

def get_players(db: Session, skip: int = 0, limit: int = 100):
    """Отримня списока гравців ."""
    return db.query(Players).offset(skip).limit(limit).all()

def get_team(db: Session, team_id: int):
    """Отримння команди за ID."""
    return db.query(Teams).filter(Teams.team_id == team_id).first()

def get_hero(db: Session, hero_id: int):
    """Отримня героя за ID."""
    return db.query(Heroes).filter(Heroes.hero_id == hero_id).first()

def get_statistics(db: Session, stat_id: int):
    """ОтримеЯ запису статистики за ID."""
    return db.query(Statistics).filter(Statistics.stat_id == stat_id).first()

def get_player_stats(db: Session, player_id: int):
    """Отримує всю статистику для конкретного гравця."""
    return db.query(Statistics).filter(Statistics.player_id == player_id).all()

# ====================== UPDATE ======================

def update_player_nickname(db: Session, player_id: int, new_nickname: str):
    """Оновлює нік гравця."""
    db_player = db.query(Players).filter(Players.player_id == player_id).first()
    if db_player:
        db_player.nickname = new_nickname
        db.commit()
        db.refresh(db_player)
    return db_player

def make_player_available(db: Session, player_id: int, available: bool = True):
    """Змінює статус доступності гравця."""
    db_player = db.query(Players).filter(Players.player_id == player_id).first()
    if db_player:
        db_player.available = available
        db.commit()
        db.refresh(db_player)
    return db_player

# ====================== DELETE ======================

def delete_player(db: Session, player_id: int):
    """Видаляє гравця за ID."""
    db_player = db.query(Players).filter(Players.player_id == player_id).first()
    if db_player:
        db.delete(db_player)
        db.commit()
        return True
    return False

def delete_team(db: Session, team_id: int):
    """Видаляє команду за ID."""
    db_team = db.query(Teams).filter(Teams.team_id == team_id).first()
    if db_team:
        db.delete(db_team)
        db.commit()
        return True
    return False

def delete_statistics_record(db: Session, stat_id: int):
    """Видаляє запис статистики за ID."""
    db_stat = db.query(Statistics).filter(Statistics.stat_id == stat_id).first()
    if db_stat:
        db.delete(db_stat)
        db.commit()
        return True
    return False
    # ====================== Додаткові функції для READ ======================

def get_teams(db: Session, skip: int = 0, limit: int = 100) -> List[Teams]:
    return db.query(Teams).offset(skip).limit(limit).all()

def get_heroes(db: Session, skip: int = 0, limit: int = 100) -> List[Heroes]:
    return db.query(Heroes).offset(skip).limit(limit).all()

def get_tournaments(db: Session, skip: int = 0, limit: int = 100) -> List[Tournaments]:
    return db.query(Tournaments).offset(skip).limit(limit).all()

def get_tournament(db: Session, tournament_id: int) -> Optional[Tournaments]:
    return db.query(Tournaments).filter(Tournaments.tournament_id == tournament_id).first()

def get_match(db: Session, match_id: int) -> Optional[Matches]:
    return db.query(Matches).filter(Matches.match_id == match_id).first()

def get_matches(db: Session, skip: int = 0, limit: int = 100) -> List[Matches]:
    return db.query(Matches).offset(skip).limit(limit).all()

def get_series(db: Session, series_id: int) -> Optional[Series]:
    return db.query(Series).filter(Series.series_id == series_id).first()

def get_all_statistics(db: Session, skip: int = 0, limit: int = 100) -> List[Statistics]:
    return db.query(Statistics).offset(skip).limit(limit).all()

# ====================== Додаткові функції для CREATE ======================

def create_tournament(db: Session, name: str, start_date: Optional[date], end_date: Optional[date], winner: Optional[str]) -> Tournaments:
    db_tournament = Tournaments(name=name, start_date=start_date, end_date=end_date, winner=winner)
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament

def create_match(db: Session, series_id: int, tournament_id: int, team_radiant: int, team_dire: int, winner_id: int) -> Matches:
    db_match = Matches(
        series_id=series_id,
        tournament_id=tournament_id,
        team_radiant=team_radiant,
        team_dire=team_dire,
        winner_id=winner_id
    )
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

# ====================== Додаткові функції для DELETE ======================

def delete_tournament(db: Session, tournament_id: int) -> bool:
    db_tournament = db.query(Tournaments).filter(Tournaments.tournament_id == tournament_id).first()
    if db_tournament:
        db.delete(db_tournament)
        db.commit()
        return True
    return False

def delete_match(db: Session, match_id: int) -> bool:
    db_match = db.query(Matches).filter(Matches.match_id == match_id).first()
    if db_match:
        db.delete(db_match)
        db.commit()
        return True
    return False

def delete_hero(db: Session, hero_id: int) -> bool:
    db_hero = db.query(Heroes).filter(Heroes.hero_id == hero_id).first()
    if db_hero:
        db.delete(db_hero)
        db.commit()
        return True
    return False