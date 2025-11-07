# Dota2 Analytics — ORM (FastAPI)

README для папки `ORM` — тут знаходиться FastAPI-додаток, SQLAlchemy-моделі та CRUD-логіка.

Що в папці
- `main.py` — точка входу FastAPI (реєструє роутери).
- `routes.py` — визначення REST маршрутів (вкладені маршрути для турнірів/серій/матчів, команда→гравці, тощо).
- `controllers.py` — бізнес-логіка (виклики CRUD + перевірки).
- `crud.py` — операції з базою даних (SQLAlchemy).
- `models.py` — SQLAlchemy моделі таблиць.
- `schemas.py` — Pydantic схеми для валідації/відповідей.
- `database.py` — налаштування підключення до БД (engine, SessionLocal, Base).

Запуск (рекомендовано — з кореня проекту)
1) Встановіть залежності (у віртуальному оточенні):

```powershell
cd C:\Users\Master\Desktop\dota2-analytics-db-development\ORM
pip install -r requirements.txt
```

2) Запуск з кореня проекту (рекомендується) — це дозволяє імпортувати пакет `ORM` коректно:

```powershell
cd C:\Users\Master\Desktop\dota2-analytics-db-development
uvicorn ORM.main:app --reload --host 127.0.0.1 --port 8000
```

3) Або запустити зсередини папки `ORM` (як альтернатива):

```powershell
cd C:\Users\Master\Desktop\dota2-analytics-db-development\ORM
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Документація API
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

