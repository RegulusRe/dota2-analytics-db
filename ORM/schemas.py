from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List
from datetime import date

# --------- Базові схеми з валідацією ---------
class PlayerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255, description="Ім'я гравця")
    nickname: str = Field(..., min_length=2, max_length=255, description="Нікнейм гравця")
    position: str = Field(..., min_length=1, max_length=100, description="Позиція гравця")
    team_id: int = Field(..., gt=0, description="ID команди")

    @field_validator('position')
    @classmethod
    def validate_position(cls, v):
        valid_positions = ['Carry', 'Mid', 'Offlane', 'Support', 'Hard Support', 'Pos 1', 'Pos 2', 'Pos 3', 'Pos 4', 'Pos 5']
        if v not in valid_positions:
            raise ValueError(f'Позиція має бути одна з: {", ".join(valid_positions)}')
        return v

class TeamBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255, description="Назва команди")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Назва команди не може бути порожньою')
        return v.strip()

class HeroBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255, description="Ім'я героя")
    role: str = Field(..., min_length=2, max_length=100, description="Роль героя")
    ultimate: str = Field(..., min_length=2, max_length=255, description="Ультимейт героя")

    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        valid_roles = ['Carry', 'Support', 'Nuker', 'Disabler', 'Initiator', 'Durable', 'Escape', 'Pusher', 'Jungler']
        if v not in valid_roles:
            raise ValueError(f'Роль має бути одна з: {", ".join(valid_roles)}')
        return v

class TournamentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255, description="Назва турніру")
    start_date: Optional[date] = Field(None, description="Дата початку турніру")
    end_date: Optional[date] = Field(None, description="Дата закінчення турніру")
    winner: Optional[str] = Field(None, max_length=255, description="Переможець турніру")

    @model_validator(mode='after')
    def validate_dates(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValueError('Дата закінчення не може бути раніше дати початку')
        return self

class SeriesBase(BaseModel):
    tournament_id: int = Field(..., gt=0, description="ID турніру")
    team1_id: int = Field(..., gt=0, description="ID першої команди")
    team2_id: int = Field(..., gt=0, description="ID другої команди")
    winner_id: Optional[int] = Field(None, gt=0, description="ID команди-переможця")
    score_team1: int = Field(0, ge=0, le=3, description="Рахунок першої команди")
    score_team2: int = Field(0, ge=0, le=3, description="Рахунок другої команди")

    @model_validator(mode='after')
    def validate_series(self):
        if self.team1_id == self.team2_id:
            raise ValueError('Команди мають бути різними')
        if self.winner_id and self.winner_id not in [self.team1_id, self.team2_id]:
            raise ValueError('Переможець має бути однією з команд серії')
        return self

class MatchBase(BaseModel):
    series_id: int = Field(..., gt=0, description="ID серії")
    tournament_id: int = Field(..., gt=0, description="ID турніру")
    team_radiant: int = Field(..., gt=0, description="ID команди Radiant")
    team_dire: int = Field(..., gt=0, description="ID команди Dire")
    winner_id: int = Field(..., gt=0, description="ID команди-переможця")

    @model_validator(mode='after')
    def validate_match(self):
        if self.team_radiant == self.team_dire:
            raise ValueError('Команди Radiant і Dire мають бути різними')
        if self.winner_id not in [self.team_radiant, self.team_dire]:
            raise ValueError('Переможець має бути Radiant або Dire')
        return self

class StatisticBase(BaseModel):
    player_id: int = Field(..., gt=0, description="ID гравця")
    match_id: int = Field(..., gt=0, description="ID матчу")
    hero_id: int = Field(..., gt=0, description="ID героя")
    kills: int = Field(0, ge=0, le=100, description="Кількість вбивств")
    deaths: int = Field(0, ge=0, le=50, description="Кількість смертей")
    assists: int = Field(0, ge=0, le=100, description="Кількість асистів")
    damage: int = Field(0, ge=0, description="Завдана шкода")
    roshan_kills: int = Field(0, ge=0, le=10, description="Вбивства Рошана")
    towers_kills: int = Field(0, ge=0, le=11, description="Зруйновані вежі")

    @field_validator('towers_kills')
    @classmethod
    def validate_towers(cls, v):
        if v > 11:
            raise ValueError('Максимальна кількість веж - 11')
        return v

class PrizeBase(BaseModel):
    team_id: int = Field(..., gt=0, description="ID команди")
    tournament_id: int = Field(..., gt=0, description="ID турніру")
    amount: float = Field(..., gt=0, description="Сума призу")
    position: int = Field(..., gt=0, le=20, description="Місце команди")

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Сума призу має бути більше 0')
        if v > 100_000_000:
            raise ValueError('Сума призу занадто велика')
        return round(v, 2)

# --------- Схеми відповідей ---------
class PlayerResponse(PlayerBase):
    player_id: int

    class Config:
        from_attributes = True

class TeamResponse(TeamBase):
    team_id: int

    class Config:
        from_attributes = True

class HeroResponse(HeroBase):
    hero_id: int

    class Config:
        from_attributes = True

class TournamentResponse(TournamentBase):
    tournament_id: int

    class Config:
        from_attributes = True

class SeriesResponse(SeriesBase):
    series_id: int

    class Config:
        from_attributes = True

class MatchResponse(MatchBase):
    match_id: int

    class Config:
        from_attributes = True

class StatisticResponse(StatisticBase):
    stat_id: int

    class Config:
        from_attributes = True

class PrizeResponse(PrizeBase):
    prize_id: int

    class Config:
        from_attributes = True

# --------- Схеми для оновлення з валідацією ---------
class PlayerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    nickname: Optional[str] = Field(None, min_length=2, max_length=255)
    position: Optional[str] = Field(None, min_length=1, max_length=100)
    team_id: Optional[int] = Field(None, gt=0)

    @field_validator('position')
    @classmethod
    def validate_position(cls, v):
        if v is not None:
            valid_positions = ['Carry', 'Mid', 'Offlane', 'Support', 'Hard Support', 'Pos 1', 'Pos 2', 'Pos 3', 'Pos 4', 'Pos 5']
            if v not in valid_positions:
                raise ValueError(f'Позиція має бути одна з: {", ".join(valid_positions)}')
        return v

class TeamUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Назва команди не може бути порожньою')
        return v.strip() if v else v

class HeroUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    role: Optional[str] = Field(None, min_length=2, max_length=100)
    ultimate: Optional[str] = Field(None, min_length=2, max_length=255)

    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        if v is not None:
            valid_roles = ['Carry', 'Support', 'Nuker', 'Disabler', 'Initiator', 'Durable', 'Escape', 'Pusher', 'Jungler']
            if v not in valid_roles:
                raise ValueError(f'Роль має бути одна з: {", ".join(valid_roles)}')
        return v

class TournamentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    winner: Optional[str] = Field(None, max_length=255)

class SeriesUpdate(BaseModel):
    winner_id: Optional[int] = Field(None, gt=0)
    score_team1: Optional[int] = Field(None, ge=0, le=3)
    score_team2: Optional[int] = Field(None, ge=0, le=3)

class MatchUpdate(BaseModel):
    winner_id: Optional[int] = Field(None, gt=0)

class StatisticUpdate(BaseModel):
    kills: Optional[int] = Field(None, ge=0, le=100)
    deaths: Optional[int] = Field(None, ge=0, le=50)
    assists: Optional[int] = Field(None, ge=0, le=100)
    damage: Optional[int] = Field(None, ge=0)
    roshan_kills: Optional[int] = Field(None, ge=0, le=10)
    towers_kills: Optional[int] = Field(None, ge=0, le=11)

class PrizeUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    position: Optional[int] = Field(None, gt=0, le=20)

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v is not None:
            if v > 100_000_000:
                raise ValueError('Сума призу занадто велика')
            return round(v, 2)
        return v