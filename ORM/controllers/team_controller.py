from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import *
from schemas import TeamCreate, TeamUpdate, TeamResponse

router = APIRouter(
    prefix="/teams",
    tags=["teams"]
)

@router.post("/", response_model=TeamResponse)
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    return create_team(db, team.name)

@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: int, db: Session = Depends(get_db)):
    db_team = get_team(db, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Команду не знайдено")
    return db_team

@router.get("/", response_model=List[TeamResponse])
def get_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_teams(db, skip=skip, limit=limit)

@router.put("/{team_id}", response_model=TeamResponse)
def update_team(team_id: int, team_update: TeamUpdate, db: Session = Depends(get_db)):
    db_team = get_team(db, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Команду не знайдено")
    for key, value in team_update.dict(exclude_unset=True).items():
        setattr(db_team, key, value)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.delete("/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    success = delete_team(db, team_id)
    if not success:
        raise HTTPException(status_code=404, detail="Команду не знайдено")
    return {"detail": "Команду видалено"}