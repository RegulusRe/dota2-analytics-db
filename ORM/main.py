from sqlalchemy.orm import Session
from database import SessionLocal
from crud import (
    create_player,
    get_player,
    get_players,
    update_player_nickname,
    delete_player
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def main():
    print("=== Початок main.py ===")
    db: Session = next(get_db())

    print("\n--- 1. Створити нового гравця ---")
    new_player = create_player(db, "Test Player", "TestNick", "Mid", 9565)
    print(f"✅ Створено: {new_player.name} (ID: {new_player.player_id})")

    print("\n--- 2. Отримати гравця за ID ---")
    player = get_player(db, new_player.player_id)
    if player:
        print(f"✅ Знайдено: {player.name} ({player.nickname})")

    print("\n--- 3. Отримати список гравців ---")
    players = get_players(db)
    for p in players:
        print(f"  - {p.name} ({p.nickname})")

    print("\n--- 4. Оновити нік гравця ---")
    updated_player = update_player_nickname(db, new_player.player_id, "UpdatedNick123")
    if updated_player:
        print(f"✅ Оновлено: {updated_player.nickname}")

    print("\n--- 5. Видалити гравця ---")
    is_deleted = delete_player(db, new_player.player_id)
    if is_deleted:
        print("✅ Гравця видалено")

    db.close()
    print("\n=== Кінець main.py ===")

if __name__ == "__main__":
    main()