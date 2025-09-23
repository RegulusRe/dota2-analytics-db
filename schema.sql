-- =============================================
-- ОНОВЛЕНА СТРУКТУРА БАЗИ ДАНИХ (BIGINT для всіх ID)
-- Для роботи з реальними даними Dota 2 (TI, FISSURE тощо)
-- =============================================

-- Таблиця турнірів
CREATE TABLE `Tournaments` (
  `tournament_id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255),
  `start_date` DATE,
  `end_date` DATE,
  `winner` VARCHAR(255)
);

-- Таблиця команд
CREATE TABLE `Teams` (
  `team_id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) UNIQUE
);

-- Таблиця гравців
CREATE TABLE `Players` (
  `player_id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255),
  `nickname` VARCHAR(255),
  `position` VARCHAR(255),
  `team_id` BIGINT
);

-- Таблиця героїв
CREATE TABLE `Heroes` (
  `hero_id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) UNIQUE,
  `role` VARCHAR(255),
  `ultimate` VARCHAR(255)
);

-- Таблиця серій
CREATE TABLE `Series` (
  `series_id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `tournament_id` BIGINT,
  `team1_id` BIGINT,
  `team2_id` BIGINT,
  `winner_id` BIGINT
);

-- Таблиця матчів
CREATE TABLE `Matches` (
  `match_id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `series_id` BIGINT,
  `tournament_id` BIGINT,
  `team_radiant` BIGINT,
  `team_dire` BIGINT,
  `winner_id` BIGINT
);

-- Таблиця статистики
CREATE TABLE `Statistics` (
  `stat_id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `player_id` BIGINT,
  `match_id` BIGINT,
  `hero_id` BIGINT,
  `kills` INT,
  `deaths` INT,
  `assists` INT,
  `damage` INT,
  `roshan_kills` INT,
  `towers_kills` INT
);

-- Таблиця призів
CREATE TABLE `Prizes` (
  `prize_id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `tournament_id` BIGINT,
  `team_id` BIGINT,
  `place` INT,
  `amount` DECIMAL
);

-- Зовнішні ключі
ALTER TABLE `Players` ADD FOREIGN KEY (`team_id`) REFERENCES `Teams` (`team_id`) ON DELETE SET NULL;

ALTER TABLE `Series` ADD FOREIGN KEY (`tournament_id`) REFERENCES `Tournaments` (`tournament_id`) ON DELETE CASCADE;
ALTER TABLE `Series` ADD FOREIGN KEY (`team1_id`) REFERENCES `Teams` (`team_id`) ON DELETE CASCADE;
ALTER TABLE `Series` ADD FOREIGN KEY (`team2_id`) REFERENCES `Teams` (`team_id`) ON DELETE CASCADE;
ALTER TABLE `Series` ADD FOREIGN KEY (`winner_id`) REFERENCES `Teams` (`team_id`) ON DELETE CASCADE;

ALTER TABLE `Matches` ADD FOREIGN KEY (`series_id`) REFERENCES `Series` (`series_id`) ON DELETE CASCADE;
ALTER TABLE `Matches` ADD FOREIGN KEY (`tournament_id`) REFERENCES `Tournaments` (`tournament_id`) ON DELETE CASCADE;
ALTER TABLE `Matches` ADD FOREIGN KEY (`team_radiant`) REFERENCES `Teams` (`team_id`) ON DELETE CASCADE;
ALTER TABLE `Matches` ADD FOREIGN KEY (`team_dire`) REFERENCES `Teams` (`team_id`) ON DELETE CASCADE;
ALTER TABLE `Matches` ADD FOREIGN KEY (`winner_id`) REFERENCES `Teams` (`team_id`) ON DELETE CASCADE;

ALTER TABLE `Statistics` ADD FOREIGN KEY (`player_id`) REFERENCES `Players` (`player_id`) ON DELETE CASCADE;
ALTER TABLE `Statistics` ADD FOREIGN KEY (`match_id`) REFERENCES `Matches` (`match_id`) ON DELETE CASCADE;
ALTER TABLE `Statistics` ADD FOREIGN KEY (`hero_id`) REFERENCES `Heroes` (`hero_id`) ON DELETE CASCADE;

ALTER TABLE `Prizes` ADD FOREIGN KEY (`tournament_id`) REFERENCES `Tournaments` (`tournament_id`) ON DELETE CASCADE;
ALTER TABLE `Prizes` ADD FOREIGN KEY (`team_id`) REFERENCES `Teams` (`team_id`) ON DELETE CASCADE;