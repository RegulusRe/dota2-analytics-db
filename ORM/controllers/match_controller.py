from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import *
from schemas import MatchCreate, MatchUpdate, MatchResponse

router = APIRouter(
    prefix="/matches",
    tags=["matches"]
)

@router.post("/", response_model=MatchResponse)
def create_match(match: MatchCreate, db: Session = Depends(get_db)):
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

@router.get("/{match_id}", response_model=MatchResponse)
def get_match(match_id: int, db: Session = Depends(get_db)):
    db_match = get_match(db, match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Матч не знайдено")
    return db_match

@router.get("/", response_model=List[MatchResponse])
def get_matches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_matches(db, skip=skip, limit=limit)

@router.put("/{match_id}", response_model=MatchResponse)
def update_match(match_id: int, match_update: MatchUpdate, db: Session = Depends(get_db)):
    db_match = get_match(db, match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Матч не знайдено")
    for key, value in match_update.dict(exclude_unset=True).items():
        setattr(db_match, key, value)
    db.commit()
    db.refresh(db_match)
    return db_match

@router.delete("/{match_id}")
def delete_match(match_id: int, db: Session = Depends(get_db)):
    success = delete_match(db, match_id)
    if not success:
        raise HTTPException(status_code=404, detail="Матч не знайдено")
    return {"detail": "Матч видалено"}