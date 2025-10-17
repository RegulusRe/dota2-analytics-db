# 🎮 Dota 2 Analytics Database

Цей репозиторій містить структуру бази даних для аналізу турнірів та матчів у грі Dota 2, а також приклади SQL-скриптів для завантаження та експорту даних з використанням `LOAD DATA INFILE` та `SELECT ... INTO OUTFILE`.

---

## 📁 Структура репозиторію

- `schema.sql` — скрипт для створення таблиць бази даних.
- `data.sql` — SQL-запити для імпорту прикладних даних (наприклад, The International 2023).
- `views_and_queries.sql` — корисні `VIEW` та аналітичні запити.
- `README.md` — цей файл.
- `load_data_examples.sql` — приклади використання `LOAD DATA INFILE`.
- `export_data_examples.sql` — приклади використання `SELECT ... INTO OUTFILE`.

---

## 🛠️ Використання

### 1. Створення бази даних

1. Встановіть [MySQL](https://dev.mysql.com/downloads/mysql/).
2. Запустіть MySQL-сервер.
3. Відкрийте `schema.sql` у вашому MySQL-клієнті (наприклад, MySQL Workbench, phpMyAdmin або командний рядок).
4. Виконайте скрипт для створення таблиць.

### 2. Завантаження даних

Після створення таблиць, виконайте скрипт `data.sql`, щоб заповнити базу прикладними даними.

### 3. Приклади запитів

Файл `views_and_queries.sql` містить корисні `VIEW` для зручного аналізу, наприклад:

- `SELECT * FROM MatchDetails;` — матчі з іменами команд.
- `SELECT * FROM PlayerStats;` — статистика гравців з іменами та героями.

---

## 📥 Завантаження даних з файлу (`LOAD DATA INFILE`)

Приклад завантаження даних з текстового файлу:

```sql
LOAD DATA LOCAL INFILE 'path/to/your/file.csv'
INTO TABLE Players
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
