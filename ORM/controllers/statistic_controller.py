from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import *
from schemas import StatisticCreate, StatisticUpdate, StatisticResponse

router = APIRouter(
    prefix="/statistics",
    tags=["statistics"]
)

@router.post("/", response_model=StatisticResponse)
def create_statistic(stat: StatisticCreate, db: Session = Depends(get_db)):
    # Перевірка існування зовнішніх ключів
    if not get_player(db, stat.player_id):
        raise HTTPException(status_code=404, detail="Гравця не знайдено")
    if not get_match(db, stat.match_id):
        raise HTTPException(status_code=404, detail="Матч не знайдено")
    if not get_hero(db, stat.hero_id):
        raise HTTPException(status_code=404, detail="Героя не знайдено")

    return create_statistics_record(
        db,
        stat.player_id,
        stat.match_id,
        stat.hero_id,
        stat.kills,
        stat.deaths,
        stat.assists,
        stat.damage,
        stat.roshan_kills,
        stat.towers_kills
    )

@router.get("/{stat_id}", response_model=StatisticResponse)
def get_statistic(stat_id: int, db: Session = Depends(get_db)):
    db_stat = get_statistics(db, stat_id)
    if not db_stat:
        raise HTTPException(status_code=404, detail="Статистику не знайдено")
    return db_stat

@router.get("/", response_model=List[StatisticResponse])
def get_statistics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_statistics(db, skip=skip, limit=limit)

@router.put("/{stat_id}", response_model=StatisticResponse)
def update_statistic(stat_id: int, stat_update: StatisticUpdate, db: Session = Depends(get_db)):
    db_stat = get_statistics(db, stat_id)
    if not db_stat:
        raise HTTPException(status_code=404, detail="Статистику не знайдено")
    for key, value in stat_update.dict(exclude_unset=True).items():
        if value is not None:  # Оновлюємо тільки якщо значення передано
            setattr(db_stat, key, value)
    db.commit()
    db.refresh(db_stat)
    return db_stat

@router.delete("/{stat_id}")
def delete_statistic(stat_id: int, db: Session = Depends(get_db)):
    success = delete_statistics_record(db, stat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Статистику не знайдено")
    return {"detail": "Статистику видалено"}