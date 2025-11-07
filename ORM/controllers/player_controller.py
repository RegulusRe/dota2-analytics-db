from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import *
from schemas import PlayerCreate, PlayerUpdate, PlayerResponse

router = APIRouter(
    prefix="/players",
    tags=["players"]
)

@router.post("/", response_model=PlayerResponse)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    db_team = get_team(db, player.team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Команда не знайдена")
    return create_player(db, player.name, player.nickname, player.position, player.team_id)

@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(player_id: int, db: Session = Depends(get_db)):
    db_player = get_player(db, player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Гравця не знайдено")
    return db_player

@router.get("/", response_model=List[PlayerResponse])
def get_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_players(db, skip=skip, limit=limit)

@router.put("/{player_id}", response_model=PlayerResponse)
def update_player(player_id: int, player_update: PlayerUpdate, db: Session = Depends(get_db)):
    db_player = get_player(db, player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Гравця не знайдено")
    if player_update.nickname is not None:
        updated_player = update_player_nickname(db, player_id, player_update.nickname)
        if not updated_player:
            raise HTTPException(status_code=404, detail="Не вдалося оновити гравця")
        return updated_player
    return db_player

@router.delete("/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    success = delete_player(db, player_id)
    if not success:
        raise HTTPException(status_code=404, detail="Гравця не знайдено")
    return {"detail": "Гравця видалено"}