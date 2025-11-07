from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from database import SessionLocal
from crud import *
from models import Players

app = FastAPI(title="Dota 2 API", description="API для управління базою даних  Dota 2")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PlayerBase(BaseModel):
    name: str
    nickname: str
    position: str
    team_id: int

class PlayerUpdate(BaseModel):
    nickname: Optional[str] = None

class PlayerResponse(PlayerBase):
    player_id: int

    class Config:
        from_attributes = True

# --- TEAM ---
class TeamBase(BaseModel):
    name: str

class TeamResponse(TeamBase):
    team_id: int

    class Config:
        from_attributes = True


# --- HERO ---
class HeroBase(BaseModel):
    name: str
    role: str
    ultimate: str

class HeroResponse(HeroBase):
    hero_id: int

    class Config:
        from_attributes = True


# --- TOURNAMENT ---
class TournamentBase(BaseModel):
    name: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    winner: Optional[str] = None


class TournamentResponse(TournamentBase):
    tournament_id: int

    class Config:
        from_attributes = True


# --- MATCH ---
class MatchBase(BaseModel):
    series_id: int
    tournament_id: int
    team_radiant: int
    team_dire: int
    winner_id: int


class MatchResponse(MatchBase):
    match_id: int

    class Config:
        from_attributes = True


# --- STATISTIC ---
class StatisticBase(BaseModel):
    player_id: int
    match_id: int
    hero_id: int
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    damage: int = 0
    roshan_kills: int = 0
    towers_kills: int = 0


class StatisticUpdate(BaseModel):
    kills: Optional[int] = None
    deaths: Optional[int] = None
    assists: Optional[int] = None
    damage: Optional[int] = None
    roshan_kills: Optional[int] = None
    towers_kills: Optional[int] = None

class StatisticResponse(StatisticBase):
    stat_id: int

    class Config:
        from_attributes = True

@app.get("/")
def read_root():
    return {"message": "Ласкаво просимо до Dota 2 API!"}

# --- PLAYERS ---

@app.post("/players/", response_model=PlayerResponse)
def api_create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    db_team = get_team(db, player.team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Команда не знайдена")
    return create_player(db, player.name, player.nickname, player.position, player.team_id)

@app.get("/players/{player_id}", response_model=PlayerResponse)
def api_get_player(player_id: int, db: Session = Depends(get_db)):
    db_player = get_player(db, player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Гравця не знайдено")
    return db_player

@app.get("/players/", response_model=List[PlayerResponse])
def api_get_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_players(db, skip=skip, limit=limit)

@app.put("/players/{player_id}", response_model=PlayerResponse)
def api_update_player(player_id: int, player_update: PlayerUpdate, db: Session = Depends(get_db)):
    db_player = get_player(db, player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Гравця не знайдено")
    if player_update.nickname is not None:
        updated_player = update_player_nickname(db, player_id, player_update.nickname)
        if not updated_player:
            raise HTTPException(status_code=404, detail="Не вдалося оновити гравця")
        return updated_player
    return db_player

@app.delete("/players/{player_id}")
def api_delete_player(player_id: int, db: Session = Depends(get_db)):
    success = delete_player(db, player_id)
    if not success:
        raise HTTPException(status_code=404, detail="Гравця не знайдено")
    return {"detail": "Гравця видалено"}
    
# ===================== TEAMS =====================

@app.post("/teams/", response_model=TeamResponse)
def api_create_team(team: TeamCreate, db: Session = Depends(get_db)):
    return create_team(db, team.name)

@app.get("/teams/{team_id}", response_model=TeamResponse)
def api_get_team(team_id: int, db: Session = Depends(get_db)):
    db_team = get_team(db, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Команду не знайдено")
    return db_team

@app.get("/teams/", response_model=List[TeamResponse])
def api_get_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_teams(db, skip=skip, limit=limit)

@app.put("/teams/{team_id}", response_model=TeamResponse)
def api_update_team(team_id: int, team_update: TeamUpdate, db: Session = Depends(get_db)):
    db_team = get_team(db, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Команду не знайдено")
    for key, value in team_update.dict(exclude_unset=True).items():
        setattr(db_team, key, value)
    db.commit()
    db.refresh(db_team)
    return db_team

@app.delete("/teams/{team_id}")
def api_delete_team(team_id: int, db: Session = Depends(get_db)):
    success = delete_team(db, team_id)
    if not success:
        raise HTTPException(status_code=404, detail="Команду не знайдено")
    return {"detail": "Команду видалено"}


# ===================== HEROES =====================

@app.post("/heroes/", response_model=HeroResponse)
def api_create_hero(hero: HeroCreate, db: Session = Depends(get_db)):
    return create_hero(db, hero.name, hero.role, hero.ultimate)

@app.get("/heroes/{hero_id}", response_model=HeroResponse)
def api_get_hero(hero_id: int, db: Session = Depends(get_db)):
    db_hero = get_hero(db, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Героя не знайдено")
    return db_hero

@app.get("/heroes/", response_model=List[HeroResponse])
def api_get_heroes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_heroes(db, skip=skip, limit=limit)

@app.put("/heroes/{hero_id}", response_model=HeroResponse)
def api_update_hero(hero_id: int, hero_update: HeroUpdate, db: Session = Depends(get_db)):
    db_hero = get_hero(db, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Героя не знайдено")
    for key, value in hero_update.dict(exclude_unset=True).items():
        setattr(db_hero, key, value)
    db.commit()
    db.refresh(db_hero)
    return db_hero

@app.delete("/heroes/{hero_id}")
def api_delete_hero(hero_id: int, db: Session = Depends(get_db)):
    success = delete_hero(db, hero_id)
    if not success:
        raise HTTPException(status_code=404, detail="Героя не знайдено")
    return {"detail": "Героя видалено"}


# ===================== TOURNAMENTS =====================

@app.post("/tournaments/", response_model=TournamentResponse)
def api_create_tournament(tournament: TournamentCreate, db: Session = Depends(get_db)):
    return create_tournament(db, tournament.name, tournament.start_date, tournament.end_date, tournament.winner)

@app.get("/tournaments/{tournament_id}", response_model=TournamentResponse)
def api_get_tournament(tournament_id: int, db: Session = Depends(get_db)):
    db_tournament = get_tournament(db, tournament_id)
    if not db_tournament:
        raise HTTPException(status_code=404, detail="Турнір не знайдено")
    return db_tournament

@app.get("/tournaments/", response_model=List[TournamentResponse])
def api_get_tournaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_tournaments(db, skip=skip, limit=limit)

@app.put("/tournaments/{tournament_id}", response_model=TournamentResponse)
def api_update_tournament(tournament_id: int, tournament_update: TournamentUpdate, db: Session = Depends(get_db)):
    db_tournament = get_tournament(db, tournament_id)
    if not db_tournament:
        raise HTTPException(status_code=404, detail="Турнір не знайдено")
    for key, value in tournament_update.dict(exclude_unset=True).items():
        setattr(db_tournament, key, value)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament

@app.delete("/tournaments/{tournament_id}")
def api_delete_tournament(tournament_id: int, db: Session = Depends(get_db)):
    success = delete_tournament(db, tournament_id)
    if not success:
        raise HTTPException(status_code=404, detail="Турнір не знайдено")
    return {"detail": "Турнір видалено"}


# ===================== MATCHES =====================

@app.post("/matches/", response_model=MatchResponse)
def api_create_match(match: MatchCreate, db: Session = Depends(get_db)):
    # Перевірка існування зовнішніх ключів
    if not get_series(db, match.series_id):
        raise HTTPException(status_code=404, detail="Серію не знайдено")
    if not get_tournament(db, match.tournament_id):
        raise HTTPException(status_code=404, detail="Турнір не знайдено")
    if not get_team(db, match.team_radiant):
        raise HTTPException(status_code=404, detail="Команду Radiant не знайдено")
    if not get_team(db, match.team_dire):
        raise HTTPException(status_code=404, detail="Команду Dire не знайдено")
    if not get_team(db, match.winner_id):
        raise HTTPException(status_code=404, detail="Команду-переможця не знайдено")

    return create_match(db, match.series_id, match.tournament_id, match.team_radiant, match.team_dire, match.winner_id)

@app.get("/matches/{match_id}", response_model=MatchResponse)
def api_get_match(match_id: int, db: Session = Depends(get_db)):
    db_match = get_match(db, match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Матч не знайдено")
    return db_match

@app.get("/matches/", response_model=List[MatchResponse])
def api_get_matches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_matches(db, skip=skip, limit=limit)

@app.put("/matches/{match_id}", response_model=MatchResponse)
def api_update_match(match_id: int, match_update: MatchUpdate, db: Session = Depends(get_db)):
    db_match = get_match(db, match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Матч не знайдено")
    for key, value in match_update.dict(exclude_unset=True).items():
        setattr(db_match, key, value)
    db.commit()
    db.refresh(db_match)
    return db_match

@app.delete("/matches/{match_id}")
def api_delete_match(match_id: int, db: Session = Depends(get_db)):
    success = delete_match(db, match_id)
    if not success:
        raise HTTPException(status_code=404, detail="Матч не знайдено")
    return {"detail": "Матч видалено"}


# ===================== STATISTICS =====================

@app.post("/statistics/", response_model=StatisticResponse)
def api_create_statistic(stat: StatisticCreate, db: Session = Depends(get_db)):
    # Перевірка існування зовнішніх ключів
    if not get_player(db, stat.player_id):
        raise HTTPException(status_code=404, detail="Гравця не знайдено")
    if not get_match(db, stat.match_id):
        raise HTTPException(status_code=404, detail="Матч не знайдено")
    if not get_hero(db, stat.hero_id):
        raise HTTPException(status_code=404, detail="Героя не знайдено")

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

@app.get("/statistics/{stat_id}", response_model=StatisticResponse)
def api_get_statistic(stat_id: int, db: Session = Depends(get_db)):
    db_stat = get_statistics(db, stat_id)
    if not db_stat:
        raise HTTPException(status_code=404, detail="Статистику не знайдено")
    return db_stat

@app.get("/statistics/", response_model=List[StatisticResponse])
def api_get_statistics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_statistics(db, skip=skip, limit=limit)

@app.put("/statistics/{stat_id}", response_model=StatisticResponse)
def api_update_statistic(stat_id: int, stat_update: StatisticUpdate, db: Session = Depends(get_db)):
    db_stat = get_statistics(db, stat_id)
    if not db_stat:
        raise HTTPException(status_code=404, detail="Статистику не знайдено")
    for key, value in stat_update.dict(exclude_unset=True).items():
        if value is not None:  # Оновлюємо тільки якщо значення передано
            setattr(db_stat, key, value)
    db.commit()
    db.refresh(db_stat)
    return db_stat

@app.delete("/statistics/{stat_id}")
def api_delete_statistic(stat_id: int, db: Session = Depends(get_db)):
    success = delete_statistics_record(db, stat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Статистику не знайдено")

    return {"detail": "Статистику видалено"}
