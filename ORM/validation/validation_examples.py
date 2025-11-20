"""
Приклад використання валідаторів в API

Додайте ці імпорти в routes.py:
from .validators import *

Потім використовуйте валідатори в ендпоінтах.
"""

# ПРИКЛАД 1: Створення команди з перевіркою унікальності
"""
@team_router.post("/", response_model=TeamResponse)
async def create_team(team: TeamBase, db: Session = Depends(get_db)):
    # Перевірка унікальності назви
    validate_unique_team_name(db, team.name)
    
    # Створення команди
    return await TeamController.create(db, team)
"""

# ПРИКЛАД 2: Створення гравця з перевіркою команди
"""
@player_router.post("/", response_model=PlayerResponse)
async def create_player(player: PlayerBase, db: Session = Depends(get_db)):
    # Перевірка що команда існує
    validate_team_exists(db, player.team_id)
    
    # Створення гравця
    return await PlayerController.create(db, player)
"""

# ПРИКЛАД 3: Створення серії з валідацією команд
"""
@series_router.post("/", response_model=SeriesResponse)
async def create_series(series: SeriesBase, db: Session = Depends(get_db)):
    # Перевірка турніру
    validate_tournament_exists(db, series.tournament_id)
    
    # Перевірка команд
    validate_series_teams(db, series.team1_id, series.team2_id, series.winner_id)
    
    # Створення серії
    return await SeriesController.create(db, series)
"""

# ПРИКЛАД 4: Створення матчу з повною валідацією
"""
@match_router.post("/", response_model=MatchResponse)
async def create_match(match: MatchBase, db: Session = Depends(get_db)):
    # Перевірка серії та турніру
    validate_series_exists(db, match.series_id)
    validate_tournament_exists(db, match.tournament_id)
    validate_series_belongs_to_tournament(db, match.series_id, match.tournament_id)
    
    # Перевірка команд
    validate_match_teams(db, match.team_radiant, match.team_dire, match.winner_id)
    
    # Створення матчу
    return await MatchController.create(db, match)
"""

# ПРИКЛАД 5: Створення статистики з валідацією
"""
@statistic_router.post("/", response_model=StatisticResponse)
async def create_statistic(stat: StatisticBase, db: Session = Depends(get_db)):
    # Валідація всіх зв'язків
    validate_statistics_data(db, stat.player_id, stat.match_id, stat.hero_id)
    
    # Створення статистики
    return await StatisticController.create(db, stat)
"""

# ПРИКЛАД 6: Оновлення команди з перевіркою унікальності
"""
@team_router.put("/{team_id}", response_model=TeamResponse)
async def update_team(team_id: int, team: TeamUpdate, db: Session = Depends(get_db)):
    # Перевірка існування
    validate_team_exists(db, team_id)
    
    # Якщо змінюється назва - перевіряємо унікальність
    if team.name:
        validate_unique_team_name(db, team.name, exclude_id=team_id)
    
    # Оновлення
    return await TeamController.update(db, team_id, team)
"""
