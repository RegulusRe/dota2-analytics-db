# 🎮 Dota 2 Analytics Database

📊 Проект для аналізу даних Dota 2 — з реальними даними The International 2023.

## ✅ Що включено:

- Структура бази даних (`schema.sql`)
- Дані з TI2023 (`data.sql`)
- VIEW для зручного перегляду з іменами (`views_and_queries.sql`)
- Аналітичні запити: топ гравців, призові команд, популярні герої

## 🛠 Як використовувати:

1. Створи базу в MySQL
2. Виконай `schema.sql`
3. Виконай `data.sql`
4. Виконай `views_and_queries.sql`
5. Аналізуй через `SELECT * FROM MatchDetails;` та інші VIEW

## 📈 Приклади запитів:

```sql
SELECT * FROM PlayerStats WHERE kills > 10;
SELECT * FROM PrizeSummary ORDER BY prize_amount DESC;