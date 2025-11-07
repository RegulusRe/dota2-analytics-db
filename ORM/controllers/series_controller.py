from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import *
from schemas import SeriesCreate, SeriesUpdate, SeriesResponse, MatchCreate, MatchResponse

router = APIRouter(
    tags=["series"]
)

@router.get("/tournaments/{tournament_id}/series/{series_id}", response_model=SeriesResponse)
def get_series(
    tournament_id: int,
    series_id: int,
    db: Session = Depends(get_db)
):
    db_tournament = get_tournament(db, tournament_id)
    if not db_tournament:
        raise HTTPException(status_code=404, detail="Турнір не знайдено")
    db_series = get_series(db, series_id)
    if not db_series or db_series.tournament_id != tournament_id:
        raise HTTPException(status_code=404, detail="Серію не знайдено")
    return db_series

@router.put("/tournaments/{tournament_id}/series/{series_id}", response_model=SeriesResponse)
def update_series(
    tournament_id: int,
    series_id: int,
    series_update: SeriesUpdate,
    db: Session = Depends(get_db)
):
    db_tournament = get_tournament(db, tournament_id)
    if not db_tournament:
        raise HTTPException(status_code=404, detail="Турнір не знайдено")
    db_series = get_series(db, series_id)
    if not db_series or db_series.tournament_id != tournament_id:
        raise HTTPException(status_code=404, detail="Серію не знайдено")
    return update_series(db, series_id, series_update)

# Вкладені маршрути для матчів
@router.post("/tournaments/{tournament_id}/series/{series_id}/matches/", response_model=MatchResponse)
def create_series_match(
    tournament_id: int,
    series_id: int,
    match: MatchCreate,
    db: Session = Depends(get_db)
):
    db_tournament = get_tournament(db, tournament_id)
    if not db_tournament:
        raise HTTPException(status_code=404, detail="Турнір не знайдено")
    db_series = get_series(db, series_id)
    if not db_series or db_series.tournament_id != tournament_id:
        raise HTTPException(status_code=404, detail="Серію не знайдено")
    
    # Перевірка команд
    if not get_team(db, match.team_radiant):
        raise HTTPException(status_code=404, detail="Команду Radiant не знайдено")
    if not get_team(db, match.team_dire):
        raise HTTPException(status_code=404, detail="Команду Dire не знайдено")
    if not get_team(db, match.winner_id):
        raise HTTPException(status_code=404, detail="Команду-переможця не знайдено")

    return create_match(
        db, 
        series_id, 
        tournament_id, 
        match.team_radiant, 
        match.team_dire, 
        match.winner_id
    )

@router.get("/tournaments/{tournament_id}/series/{series_id}/matches/", response_model=List[MatchResponse])
def get_series_matches(
    tournament_id: int,
    series_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    db_tournament = get_tournament(db, tournament_id)
    if not db_tournament:
        raise HTTPException(status_code=404, detail="Турнір не знайдено")
    db_series = get_series(db, series_id)
    if not db_series or db_series.tournament_id != tournament_id:
        raise HTTPException(status_code=404, detail="Серію не знайдено")
    return get_matches_by_series(db, series_id, skip=skip, limit=limit)

@router.delete("/tournaments/{tournament_id}/series/{series_id}")
def delete_series(
    tournament_id: int,
    series_id: int,
    db: Session = Depends(get_db)
):
    db_tournament = get_tournament(db, tournament_id)
    if not db_tournament:
        raise HTTPException(status_code=404, detail="Турнір не знайдено")
    db_series = get_series(db, series_id)
    if not db_series or db_series.tournament_id != tournament_id:
        raise HTTPException(status_code=404, detail="Серію не знайдено")
    success = delete_series(db, series_id)
    if not success:
        raise HTTPException(status_code=404, detail="Не вдалося видалити серію")
    return {"detail": "Серію видалено"}