from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# --------- Базові схеми ---------
class PlayerBase(BaseModel):
    name: str
    nickname: str
    position: str
    team_id: int

class TeamBase(BaseModel):
    name: str

class HeroBase(BaseModel):
    name: str
    role: str
    ultimate: str

class TournamentBase(BaseModel):
    name: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    winner: Optional[str] = None

class SeriesBase(BaseModel):
    tournament_id: int
    team1_id: int
    team2_id: int
    winner_id: Optional[int] = None
    score_team1: int = 0
    score_team2: int = 0

class MatchBase(BaseModel):
    series_id: int
    tournament_id: int
    team_radiant: int
    team_dire: int
    winner_id: int

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

class PrizeBase(BaseModel):
    team_id: int
    tournament_id: int
    amount: float
    position: int

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

# --------- Схеми для оновлення ---------
class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    nickname: Optional[str] = None
    position: Optional[str] = None
    team_id: Optional[int] = None

class TeamUpdate(BaseModel):
    name: Optional[str] = None

class HeroUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    ultimate: Optional[str] = None

class TournamentUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    winner: Optional[str] = None

class SeriesUpdate(BaseModel):
    winner_id: Optional[int] = None
    score_team1: Optional[int] = None
    score_team2: Optional[int] = None

class MatchUpdate(BaseModel):
    winner_id: Optional[int] = None

class StatisticUpdate(BaseModel):
    kills: Optional[int] = None
    deaths: Optional[int] = None
    assists: Optional[int] = None
    damage: Optional[int] = None
    roshan_kills: Optional[int] = None
    towers_kills: Optional[int] = None