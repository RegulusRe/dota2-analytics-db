from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import *
from schemas import PrizeCreate, PrizeUpdate, PrizeResponse

router = APIRouter(
    tags=["prizes"]
)

@router.post("/teams/{team_id}/prizes/", response_model=PrizeResponse)
def create_prize(
    team_id: int,
    prize: PrizeCreate,
    db: Session = Depends(get_db)
):
    db_team = get_team(db, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Команду не знайдено")
    return create_team_prize(db, team_id, prize.tournament_id, prize.amount, prize.position)

@router.get("/teams/{team_id}/prizes/", response_model=List[PrizeResponse])
def get_team_prizes(
    team_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    db_team = get_team(db, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Команду не знайдено")
    return get_prizes_by_team(db, team_id, skip=skip, limit=limit)

@router.get("/tournaments/{tournament_id}/prizes/", response_model=List[PrizeResponse])
def get_tournament_prizes(
    tournament_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    db_tournament = get_tournament(db, tournament_id)
    if not db_tournament:
        raise HTTPException(status_code=404, detail="Турнір не знайдено")
    return get_prizes_by_tournament(db, tournament_id, skip=skip, limit=limit)

@router.put("/teams/{team_id}/prizes/{prize_id}", response_model=PrizeResponse)
def update_prize(
    team_id: int,
    prize_id: int,
    prize_update: PrizeUpdate,
    db: Session = Depends(get_db)
):
    db_team = get_team(db, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Команду не знайдено")
    db_prize = get_prize(db, prize_id)
    if not db_prize or db_prize.team_id != team_id:
        raise HTTPException(status_code=404, detail="Приз не знайдено")
    return update_team_prize(db, prize_id, prize_update)