from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import *
from schemas import TournamentCreate, TournamentUpdate, TournamentResponse

router = APIRouter(
    prefix="/tournaments",
    tags=["tournaments"]
)

@router.post("/", response_model=TournamentResponse)
def create_tournament(tournament: TournamentCreate, db: Session = Depends(get_db)):
    return create_tournament(db, tournament.name, tournament.start_date, tournament.end_date, tournament.winner)

@router.get("/{tournament_id}", response_model=TournamentResponse)
def get_tournament(tournament_id: int, db: Session = Depends(get_db)):
    db_tournament = get_tournament(db, tournament_id)
    if not db_tournament:
        raise HTTPException(status_code=404, detail="Турнір не знайдено")
    return db_tournament

@router.get("/", response_model=List[TournamentResponse])
def get_tournaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_tournaments(db, skip=skip, limit=limit)

@router.put("/{tournament_id}", response_model=TournamentResponse)
def update_tournament(tournament_id: int, tournament_update: TournamentUpdate, db: Session = Depends(get_db)):
    db_tournament = get_tournament(db, tournament_id)
    if not db_tournament:
        raise HTTPException(status_code=404, detail="Турнір не знайдено")
    for key, value in tournament_update.dict(exclude_unset=True).items():
        setattr(db_tournament, key, value)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament

@router.delete("/{tournament_id}")
def delete_tournament(tournament_id: int, db: Session = Depends(get_db)):
    success = delete_tournament(db, tournament_id)
    if not success:
        raise HTTPException(status_code=404, detail="Турнір не знайдено")
    return {"detail": "Турнір видалено"}