from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import *
from schemas import HeroCreate, HeroUpdate, HeroResponse

router = APIRouter(
    prefix="/heroes",
    tags=["heroes"]
)

@router.post("/", response_model=HeroResponse)
def create_hero(hero: HeroCreate, db: Session = Depends(get_db)):
    return create_hero(db, hero.name, hero.role, hero.ultimate)

@router.get("/{hero_id}", response_model=HeroResponse)
def get_hero(hero_id: int, db: Session = Depends(get_db)):
    db_hero = get_hero(db, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Героя не знайдено")
    return db_hero

@router.get("/", response_model=List[HeroResponse])
def get_heroes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_heroes(db, skip=skip, limit=limit)

@router.put("/{hero_id}", response_model=HeroResponse)
def update_hero(hero_id: int, hero_update: HeroUpdate, db: Session = Depends(get_db)):
    db_hero = get_hero(db, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Героя не знайдено")
    for key, value in hero_update.dict(exclude_unset=True).items():
        setattr(db_hero, key, value)
    db.commit()
    db.refresh(db_hero)
    return db_hero

@router.delete("/{hero_id}")
def delete_hero(hero_id: int, db: Session = Depends(get_db)):
    success = delete_hero(db, hero_id)
    if not success:
        raise HTTPException(status_code=404, detail="Героя не знайдено")
    return {"detail": "Героя видалено"}