# main.py

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Players, Teams, Heroes, Statistics, Tournaments, Matches, Series, Prizes

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def main():
    print("=== Початок виконання main.py ===")
    
    # Отримуємо сесію
    db: Session = next(get_db())

    try:
        print("\n--- 1. Отримати всіх гравців і їх команди ---")
        players = db.query(Players).join(Teams).all()
        for p in players[:5]: # Показуємо перших 5
            print(f"  Гравець: {p.name} ({p.nickname}), Команда: {p.team.name}")

        print("\n--- 2. Отримати турнір ---")
        tournament = db.query(Tournaments).filter(Tournaments.tournament_id == 15476).first()
        if tournament:
            print(f"  Турнір: {tournament.name}")

        print("\n--- 3. Отримати команди ---")
        teams = db.query(Teams).all()
        print(f"  Знайдено {len(teams)} команд")

        print("\n--- 4. Отримати першого гравця (ID=100000001) ---")
        player = db.query(Players).filter(Players.player_id == 100000001).first()
        if player:
            print(f"  Гравець: {player.name} ({player.nickname})")

        print("\n--- 5. Отримати статистику гравця (ID=100000001) ---")
        stats = db.query(Statistics).filter(Statistics.player_id == 100000001).all()
        print(f"  Знайдено {len(stats)} записів статистики")

        print("\n--- 6. Отримати призові місця ---")
        prizes = db.query(Prizes).filter(Prizes.tournament_id == 15476).all()
        for p in prizes:
            team = db.query(Teams).filter(Teams.team_id == p.team_id).first()
            print(f"  Місце {p.place}: {team.name if team else 'N/A'} - ${p.amount}")

    except Exception as e:
        print(f"❌ Помилка: {e}")
    finally:
        db.close()
        print("\n=== Кінець виконання main.py ===")

if __name__ == "__main__":
    main()