from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .database import get_db
from .models import *
from .schemas import *
from .controllers import *
from .crud import *

# Створюємо роутери для кожної основної сутності
tournament_router = APIRouter(prefix="/tournaments", tags=["Tournaments"])
team_router = APIRouter(prefix="/teams", tags=["Teams"])
player_router = APIRouter(prefix="/players", tags=["Players"])
hero_router = APIRouter(prefix="/heroes", tags=["Heroes"])
match_router = APIRouter(prefix="/matches", tags=["Matches"])

# --------- Маршрути для турнірів ---------
@tournament_router.get("/", response_model=List[TournamentResponse])
async def get_tournaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Отримати список всіх турнірів"""
    return await TournamentController.get_all(db, skip, limit)

@tournament_router.post("/", response_model=TournamentResponse)
async def create_tournament(tournament: TournamentBase, db: Session = Depends(get_db)):
    """Створити новий турнір"""
    return await TournamentController.create(db, tournament)

@tournament_router.get("/{tournament_id}", response_model=TournamentResponse)
async def get_tournament(tournament_id: int, db: Session = Depends(get_db)):
    """Отримати інформацію про конкретний турнір"""
    return await TournamentController.get_by_id(db, tournament_id)


@tournament_router.put("/{tournament_id}", response_model=TournamentResponse)
async def update_tournament(tournament_id: int, tournament: TournamentUpdate, db: Session = Depends(get_db)):
    db_t = get_tournament(db, tournament_id)
    if not db_t:
        raise HTTPException(status_code=404, detail="Турнір не знайдено")
    for key, value in tournament.dict(exclude_unset=True).items():
        setattr(db_t, key, value)
    db.commit()
    db.refresh(db_t)
    return db_t


@tournament_router.delete("/{tournament_id}")
async def delete_tournament_endpoint(tournament_id: int, db: Session = Depends(get_db)):
    success = delete_tournament(db, tournament_id)
    if not success:
        raise HTTPException(status_code=404, detail="Турнір не знайдено")
    return {"detail": "Турнір видалено"}

# Вкладені маршрути для серій в турнірі
@tournament_router.get("/{tournament_id}/series", response_model=List[SeriesResponse])
async def get_tournament_series(tournament_id: int, db: Session = Depends(get_db)):
    """Отримати всі серії конкретного турніру"""
    return await SeriesController.get_by_tournament(db, tournament_id)

@tournament_router.post("/{tournament_id}/series", response_model=SeriesResponse)
async def create_tournament_series(tournament_id: int, series: SeriesBase, db: Session = Depends(get_db)):
    """Створити нову серію в турнірі"""
    return await SeriesController.create(db, tournament_id, series)


@tournament_router.get("/{tournament_id}/series/{series_id}", response_model=SeriesResponse)
async def get_series_by_id(tournament_id: int, series_id: int, db: Session = Depends(get_db)):
    s = get_series(db, series_id)
    if not s or s.tournament_id != tournament_id:
        raise HTTPException(status_code=404, detail="Серію не знайдено в цьому турнірі")
    return s


@tournament_router.put("/{tournament_id}/series/{series_id}", response_model=SeriesResponse)
async def update_series(tournament_id: int, series_id: int, series_update: SeriesUpdate, db: Session = Depends(get_db)):
    s = get_series(db, series_id)
    if not s or s.tournament_id != tournament_id:
        raise HTTPException(status_code=404, detail="Серію не знайдено в цьому турнірі")
    for key, value in series_update.dict(exclude_unset=True).items():
        setattr(s, key, value)
    db.commit()
    db.refresh(s)
    return s


@tournament_router.delete("/{tournament_id}/series/{series_id}")
async def delete_series(tournament_id: int, series_id: int, db: Session = Depends(get_db)):
    s = get_series(db, series_id)
    if not s or s.tournament_id != tournament_id:
        raise HTTPException(status_code=404, detail="Серію не знайдено в цьому турнірі")
    db.delete(s)
    db.commit()
    return {"detail": "Серію видалено"}

# Вкладені маршрути для матчів в серії
@tournament_router.get("/{tournament_id}/series/{series_id}/matches", response_model=List[MatchResponse])
async def get_series_matches(tournament_id: int, series_id: int, db: Session = Depends(get_db)):
    """Отримати всі матчі конкретної серії"""
    return await MatchController.get_by_series(db, series_id)

@tournament_router.get("/{tournament_id}/series/{series_id}/matches/{match_id}", response_model=MatchResponse)
async def get_series_match(tournament_id: int, series_id: int, match_id: int, db: Session = Depends(get_db)):
    m = get_match(db, match_id)
    if not m or m.series_id != series_id or m.tournament_id != tournament_id:
        raise HTTPException(status_code=404, detail="Матч не знайдено в цій серії")
    return m

@tournament_router.put("/{tournament_id}/series/{series_id}/matches/{match_id}", response_model=MatchResponse)
async def update_series_match(tournament_id: int, series_id: int, match_id: int, match_update: MatchUpdate, db: Session = Depends(get_db)):
    m = get_match(db, match_id)
    if not m or m.series_id != series_id:
        raise HTTPException(status_code=404, detail="Матч не знайдено в цій серії")
    for key, value in match_update.dict(exclude_unset=True).items():
        setattr(m, key, value)
    db.commit()
    db.refresh(m)
    return m

@tournament_router.delete("/{tournament_id}/series/{series_id}/matches/{match_id}")
async def delete_series_match(tournament_id: int, series_id: int, match_id: int, db: Session = Depends(get_db)):
    m = get_match(db, match_id)
    if not m or m.series_id != series_id:
        raise HTTPException(status_code=404, detail="Матч не знайдено в цій серії")
    db.delete(m)
    db.commit()
    return {"detail": "Матч видалено"}

# --------- Маршрути для команд ---------
@team_router.get("/", response_model=List[TeamResponse])
async def get_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Отримати список всіх команд"""
    return await TeamController.get_all(db, skip, limit)

@team_router.post("/", response_model=TeamResponse)
async def create_team(team: TeamBase, db: Session = Depends(get_db)):
    """Створити нову команду"""
    return await TeamController.create(db, team)

# Вкладені маршрути для гравців команди
@team_router.get("/{team_id}/players", response_model=List[PlayerResponse])
async def get_team_players(team_id: int, db: Session = Depends(get_db)):
    """Отримати всіх гравців команди"""
    return await PlayerController.get_by_team(db, team_id)

@team_router.post("/{team_id}/players", response_model=PlayerResponse)
async def add_team_player(team_id: int, player: PlayerBase, db: Session = Depends(get_db)):
    """Додати гравця до команди"""
    return await PlayerController.create(db, team_id, player)


@player_router.post("/", response_model=PlayerResponse)
async def create_player_global(player: PlayerBase, db: Session = Depends(get_db)):
    team = get_team(db, player.team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Команда не знайденa")
    return create_player(db, player.name, player.nickname, player.position, player.team_id)


@player_router.get("/", response_model=List[PlayerResponse])
async def list_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_players(db, skip=skip, limit=limit)


@player_router.get("/{player_id}", response_model=PlayerResponse)
async def get_player_detail(player_id: int, db: Session = Depends(get_db)):
    p = get_player(db, player_id)
    if not p:
        raise HTTPException(status_code=404, detail="Гравця не знайдено")
    return p


@player_router.put("/{player_id}", response_model=PlayerResponse)
async def update_player(player_id: int, player_update: PlayerUpdate, db: Session = Depends(get_db)):
    p = get_player(db, player_id)
    if not p:
        raise HTTPException(status_code=404, detail="Гравця не знайдено")
    for key, value in player_update.dict(exclude_unset=True).items():
        setattr(p, key, value)
    db.commit()
    db.refresh(p)
    return p


@player_router.delete("/{player_id}")
async def delete_player_endpoint(player_id: int, db: Session = Depends(get_db)):
    success = delete_player(db, player_id)
    if not success:
        raise HTTPException(status_code=404, detail="Гравця не знайдено")
    return {"detail": "Гравця видалено"}

# Вкладені маршрути для призів команди
@team_router.get("/{team_id}/prizes", response_model=List[PrizeResponse])
async def get_team_prizes(team_id: int, db: Session = Depends(get_db)):
    """Отримати всі призи команди"""
    return await PrizeController.get_by_team(db, team_id)


@team_router.post("/{team_id}/prizes", response_model=PrizeResponse)
async def create_team_prize(team_id: int, prize: PrizeBase, db: Session = Depends(get_db)):
    """Створити приз для команди"""
    if not get_team(db, team_id):
        raise HTTPException(status_code=404, detail="Команду не знайдено")
    return create_prize(db, team_id, prize.tournament_id, prize.amount, prize.position)

# --------- Маршрути для гравців ---------
@player_router.get("/{player_id}/statistics", response_model=List[StatisticResponse])
async def get_player_statistics(player_id: int, db: Session = Depends(get_db)):
    """Отримати статистику гравця"""
    return await StatisticsController.get_by_player(db, player_id)

# --------- Маршрути для героїв ---------
@hero_router.get("/", response_model=List[HeroResponse])
async def get_heroes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Отримати список всіх героїв"""
    return await HeroController.get_all(db, skip, limit)

@hero_router.get("/{hero_id}/statistics", response_model=List[StatisticResponse])
async def get_hero_statistics(hero_id: int, db: Session = Depends(get_db)):
    """Отримати статистику героя"""
    return await StatisticsController.get_by_hero(db, hero_id)


@hero_router.post("/", response_model=HeroResponse)
async def create_hero_global(hero: HeroBase, db: Session = Depends(get_db)):
    return create_hero(db, hero.name, hero.role, hero.ultimate)


@hero_router.get("/{hero_id}", response_model=HeroResponse)
async def get_hero_detail(hero_id: int, db: Session = Depends(get_db)):
    h = get_hero(db, hero_id)
    if not h:
        raise HTTPException(status_code=404, detail="Героя не знайдено")
    return h


@hero_router.put("/{hero_id}", response_model=HeroResponse)
async def update_hero(hero_id: int, hero_update: HeroUpdate, db: Session = Depends(get_db)):
    h = get_hero(db, hero_id)
    if not h:
        raise HTTPException(status_code=404, detail="Героя не знайдено")
    for key, value in hero_update.dict(exclude_unset=True).items():
        setattr(h, key, value)
    db.commit()
    db.refresh(h)
    return h


@hero_router.delete("/{hero_id}")
async def delete_hero_endpoint(hero_id: int, db: Session = Depends(get_db)):
    success = delete_hero(db, hero_id)
    if not success:
        raise HTTPException(status_code=404, detail="Героя не знайдено")
    return {"detail": "Героя видалено"}

# --------- Маршрути для матчів ---------
@match_router.get("/{match_id}/statistics", response_model=List[StatisticResponse])
async def get_match_statistics(match_id: int, db: Session = Depends(get_db)):
    """Отримати статистику матчу"""
    return await StatisticsController.get_by_match(db, match_id)


# --------- Статистика (глобальні CRUD) ---------
@match_router.get("/statistics/", response_model=List[StatisticResponse])
async def list_statistics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_statistics(db, skip=skip, limit=limit)


@match_router.get("/statistics/{stat_id}", response_model=StatisticResponse)
async def get_statistic(stat_id: int, db: Session = Depends(get_db)):
    s = get_statistics(db, stat_id)
    if not s:
        raise HTTPException(status_code=404, detail="Статистику не знайдено")
    return s


@match_router.post("/statistics/", response_model=StatisticResponse)
async def create_statistic(stat: StatisticBase, db: Session = Depends(get_db)):
    # validate fks
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


@match_router.put("/statistics/{stat_id}", response_model=StatisticResponse)
async def update_statistic(stat_id: int, stat_update: StatisticUpdate, db: Session = Depends(get_db)):
    s = get_statistics(db, stat_id)
    if not s:
        raise HTTPException(status_code=404, detail="Статистику не знайдено")
    for key, value in stat_update.dict(exclude_unset=True).items():
        setattr(s, key, value)
    db.commit()
    db.refresh(s)
    return s


@match_router.delete("/statistics/{stat_id}")
async def delete_statistic(stat_id: int, db: Session = Depends(get_db)):
    success = delete_statistics_record(db, stat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Статистику не знайдено")
    return {"detail": "Статистику видалено"}


@match_router.get("/", response_model=List[MatchResponse])
async def list_matches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_matches(db, skip=skip, limit=limit)


@match_router.get("/{match_id}", response_model=MatchResponse)
async def get_match_detail(match_id: int, db: Session = Depends(get_db)):
    m = get_match(db, match_id)
    if not m:
        raise HTTPException(status_code=404, detail="Матч не знайдено")
    return m


@match_router.post("/", response_model=MatchResponse)
async def create_match_global(match: MatchBase, db: Session = Depends(get_db)):
    # validate fk
    if not get_series(db, match.series_id):
        raise HTTPException(status_code=404, detail="Серію не знайдено")
    if not get_tournament(db, match.tournament_id):
        raise HTTPException(status_code=404, detail="Турнір не знайдено")
    return create_match(db, match.series_id, match.tournament_id, match.team_radiant, match.team_dire, match.winner_id)


@match_router.put("/{match_id}", response_model=MatchResponse)
async def update_match_global(match_id: int, match_update: MatchUpdate, db: Session = Depends(get_db)):
    m = get_match(db, match_id)
    if not m:
        raise HTTPException(status_code=404, detail="Матч не знайдено")
    for key, value in match_update.dict(exclude_unset=True).items():
        setattr(m, key, value)
    db.commit()
    db.refresh(m)
    return m


@match_router.delete("/{match_id}")
async def delete_match_global(match_id: int, db: Session = Depends(get_db)):
    success = delete_match(db, match_id)
    if not success:
        raise HTTPException(status_code=404, detail="Матч не знайдено")
    return {"detail": "Матч видалено"}

# Функція для реєстрації всіх роутерів
def include_routers(app):
    """Реєстрація всіх роутерів в додатку"""
    app.include_router(tournament_router)
    app.include_router(team_router)
    app.include_router(player_router)
    app.include_router(hero_router)
    app.include_router(match_router)