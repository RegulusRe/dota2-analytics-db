# Валідація для ORM Dota 2

## 📋 Огляд

Система валідації складається з двох рівнів:
1. **Pydantic валідація** (автоматична) - перевіряє типи, формати, обмеження
2. **Бізнес-логіка валідація** (ручна) - перевіряє зв'язки між сутностями, унікальність

---

## 🔍 Pydantic валідація (schemas.py)

### Автоматичні перевірки

Всі схеми мають вбудовані перевірки:

#### PlayerBase
- `name`: 2-255 символів
- `nickname`: 2-255 символів  
- `position`: має бути одна з валідних позицій (Carry, Mid, Offlane, Support, Hard Support, Pos 1-5)
- `team_id`: > 0

#### TeamBase
- `name`: 2-255 символів, не може бути порожнім

#### HeroBase
- `name`: 2-255 символів
- `role`: має бути одна з валідних ролей (Carry, Support, Nuker, Disabler, Initiator, Durable, Escape, Pusher, Jungler)
- `ultimate`: 2-255 символів

#### TournamentBase
- `name`: 2-255 символів
- `start_date` і `end_date`: дата закінчення не може бути раніше дати початку

#### SeriesBase
- `team1_id`, `team2_id`: > 0, мають бути різними
- `winner_id`: має бути однією з команд серії
- `score_team1`, `score_team2`: 0-3 (best of 3)

#### MatchBase
- `team_radiant`, `team_dire`: > 0, мають бути різними
- `winner_id`: має бути Radiant або Dire

#### StatisticBase
- `kills`: 0-100
- `deaths`: 0-50
- `assists`: 0-100
- `damage`: >= 0
- `roshan_kills`: 0-10
- `towers_kills`: 0-11 (максимум веж на карті)

#### PrizeBase
- `amount`: > 0, <= 100,000,000, округлюється до 2 знаків
- `position`: 1-20

---

## 🛡️ Бізнес-логіка валідація (validators.py)

### Валідатори існування

```python
validate_team_exists(db, team_id)           # Перевірка існування команди
validate_player_exists(db, player_id)       # Перевірка існування гравця
validate_hero_exists(db, hero_id)           # Перевірка існування героя
validate_tournament_exists(db, tournament_id) # Перевірка існування турніру
validate_series_exists(db, series_id)       # Перевірка існування серії
validate_match_exists(db, match_id)         # Перевірка існування матчу
```

### Валідатори унікальності

```python
validate_unique_team_name(db, name, exclude_id=None)  # Унікальність назви команди
validate_unique_hero_name(db, name, exclude_id=None)  # Унікальність імені героя
```

### Комплексні валідатори

```python
# Валідація команд в серії
validate_series_teams(db, team1_id, team2_id, winner_id=None)

# Валідація команд в матчі  
validate_match_teams(db, team_radiant, team_dire, winner_id)

# Перевірка що серія належить турніру
validate_series_belongs_to_tournament(db, series_id, tournament_id)

# Перевірка що гравець в команді
validate_player_in_team(db, player_id, team_id)

# Валідація статистики (перевіряє всі зв'язки + унікальність)
validate_statistics_data(db, player_id, match_id, hero_id)

# Валідація призу (перевіряє зв'язки + унікальність)
validate_prize_data(db, team_id, tournament_id, position)
```

---

## 📝 Приклади використання

### 1. Створення команди

```python
@team_router.post("/", response_model=TeamResponse)
async def create_team(team: TeamBase, db: Session = Depends(get_db)):
    # Pydantic автоматично перевірить:
    # - чи name має 2-255 символів
    # - чи name не порожній
    
    # Додаткова перевірка унікальності
    validate_unique_team_name(db, team.name)
    
    new_team = Teams(**team.dict())
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team
```

### 2. Створення гравця

```python
@player_router.post("/", response_model=PlayerResponse)
async def create_player(player: PlayerBase, db: Session = Depends(get_db)):
    # Pydantic автоматично перевірить:
    # - довжину полів
    # - що position валідна
    # - що team_id > 0
    
    # Перевірка що команда існує
    validate_team_exists(db, player.team_id)
    
    new_player = Players(**player.dict())
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player
```

### 3. Створення матчу

```python
@match_router.post("/", response_model=MatchResponse)
async def create_match(match: MatchBase, db: Session = Depends(get_db)):
    # Pydantic автоматично перевірить:
    # - що команди різні
    # - що winner_id це Radiant або Dire
    # - що всі ID > 0
    
    # Додаткові перевірки
    validate_series_exists(db, match.series_id)
    validate_tournament_exists(db, match.tournament_id)
    validate_series_belongs_to_tournament(db, match.series_id, match.tournament_id)
    validate_match_teams(db, match.team_radiant, match.team_dire, match.winner_id)
    
    new_match = Matches(**match.dict())
    db.add(new_match)
    db.commit()
    db.refresh(new_match)
    return new_match
```

### 4. Оновлення команди

```python
@team_router.put("/{team_id}", response_model=TeamResponse)
async def update_team(team_id: int, team: TeamUpdate, db: Session = Depends(get_db)):
    # Pydantic автоматично перевірить Update поля
    
    validate_team_exists(db, team_id)
    
    # Якщо змінюється назва - перевірка унікальності
    if team.name:
        validate_unique_team_name(db, team.name, exclude_id=team_id)
    
    db_team = db.query(Teams).filter(Teams.team_id == team_id).first()
    for key, value in team.dict(exclude_unset=True).items():
        setattr(db_team, key, value)
    db.commit()
    db.refresh(db_team)
    return db_team
```

---

## ❌ Обробка помилок

Всі валідатори викидають `ValidationError` (HTTP 400):

```python
# Приклад відповіді при помилці валідації
{
  "detail": "Команда з назвою 'Team Secret' вже існує"
}

# Приклад відповіді при помилці Pydantic
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "position"],
      "msg": "Позиція має бути одна з: Carry, Mid, Offlane, Support, Hard Support, Pos 1, Pos 2, Pos 3, Pos 4, Pos 5",
      "input": "InvalidPosition"
    }
  ]
}
```

---

## 🚀 Швидкий старт

1. **Імпортуйте валідатори в routes.py:**
```python
from .validators import *
```

2. **Додайте валідацію в потрібні ендпоінти** (див. validation_examples.py)

3. **Тестуйте через Swagger UI** (http://127.0.0.1:8000/docs)

---

## 📊 Переваги

✅ **Автоматична валідація** - Pydantic перевіряє дані до надходження в БД  
✅ **Зрозумілі помилки** - користувач отримує чіткі повідомлення  
✅ **Захист даних** - неможливо створити некоректні зв'язки  
✅ **Гнучкість** - легко додавати нові правила  
✅ **Документація** - автоматична генерація в Swagger UI  

Ваша ORM тепер захищена від некоректних даних! 🛡️
